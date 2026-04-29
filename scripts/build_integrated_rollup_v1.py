"""Build Product x Avenue x L11 rollup from v1 monthly sources."""
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = "/Users/propatil/Desktop/Other Projects/TPM_Related/Products Usage Metrics/Excel Analysis"
OP = os.path.join(BASE, "usage metrics op_excellence_20260420_v1.xlsx")
QS = os.path.join(BASE, "QuickSight_UsageMetrics_ExclFintech_20260420_v1.xlsx")
TBU = os.path.join(BASE, "Tableau UniquerUsers_ExclFinTech_20260420_v1.xlsx")
TBV = os.path.join(BASE, "Tableau TotalViews_ExclFinTech_20260420_v1.xlsx")
HIER = os.path.join(BASE, "das_finops_op_excellmployee_hierarchy_all.xlsx")
SHEET = "Product Rollup by L11"

AVENUE_OP = "Op Excellence"
AVENUE_DASH = "Dashboard"

QS_AXIS_ROWS = (10, 102)  # 1-indexed inclusive per user: rows 10 through 102
QS_CERBERUS_ROWS = (105, 259)

# op_excellence product -> display product
OP_PRODUCT_MAP = {}  # identity by default


def month_key(d):
    ts = pd.to_datetime(d, errors="coerce")
    return None if pd.isna(ts) else ts.strftime("%Y-%m")


def direct_parent(h):
    if not isinstance(h, str):
        return None
    parts = h.split(":")
    return parts[1] if len(parts) > 1 else None


def load_hierarchy():
    h = pd.read_excel(HIER, sheet_name="Result 1")
    h = h.dropna(subset=["login_name", "manager_login_hierarchy_concat"]).copy()
    h["chain_logins"] = h["manager_login_hierarchy_concat"].str.split(":")
    h["chain_levels"] = h["manager_job_level_hierarchy_concat"].astype(str).str.split(":")
    chain_map = {}
    for _, r in h.iterrows():
        logins = r["chain_logins"]
        levels = r["chain_levels"]
        if len(logins) != len(levels):
            continue
        chain_map[r["login_name"]] = list(zip(logins, [int(x) if x.isdigit() else None for x in levels]))
    return chain_map


def attribute_events(events_df, chain_map, login_col, product_col, month_col, views_col):
    """Return DataFrame [manager_login, product, month, distinct_users, total_views].

    events_df: one row per (login, product, month). Values in views_col are that
    user's monthly view count; distinct users is by unique login per (mgr, product, month).
    """
    rows = []
    for _, r in events_df.iterrows():
        login = r[login_col]
        product = r[product_col]
        month = r[month_col]
        views = r[views_col] if views_col else 1
        views = 0 if pd.isna(views) else float(views)
        chain = chain_map.get(login)
        if not chain:
            continue
        for mgr_login, _lvl in chain:
            rows.append({"manager_login": mgr_login, "product": product,
                         "month": month, "login": login, "views": views})
    if not rows:
        return pd.DataFrame(columns=["manager_login", "product", "month", "distinct_users", "total_views"])
    df = pd.DataFrame(rows)
    g = df.groupby(["manager_login", "product", "month"]).agg(
        distinct_users=("login", "nunique"),
        total_views=("views", "sum"),
    ).reset_index()
    return g


# -----------------------------------------------------------------------------
# Source loaders
# -----------------------------------------------------------------------------
def load_op_excellence():
    df = pd.read_excel(OP, sheet_name="Result 1")
    df["month"] = df["log_month"].apply(month_key)
    df = df[df["application_type"].notna() & df["month"].notna()]
    df = df.rename(columns={"application_type": "product"})
    agg = df.groupby(["manager_login", "product", "month"]).agg(
        distinct_users=("distinct_users", "sum"),
        total_views=("total_measure_value", "sum"),
    ).reset_index()
    agg["avenue"] = AVENUE_OP
    return agg


def parse_quicksight_section(raw, dashboard_name, start_row_1idx, end_row_1idx, month_cols):
    """Return per-user events DataFrame for one dashboard section."""
    # openpyxl/pandas use 0-indexed internally when header=None.
    # User gave 1-indexed rows (row 10 = index 9 in raw).
    start = start_row_1idx - 1
    end = end_row_1idx - 1  # inclusive
    rows = []
    for i in range(start, end + 1):
        login = raw.iloc[i, 0]
        if pd.isna(login) or not isinstance(login, str):
            continue
        for month, (li_col, en_col) in month_cols.items():
            li = raw.iloc[i, li_col]  # login_id flag
            en = raw.iloc[i, en_col]  # eventname count
            if pd.isna(li) or li == 0:
                continue
            rows.append({"login": login, "dashboard": dashboard_name,
                         "month": month, "views": float(en) if pd.notna(en) else 0.0})
    return pd.DataFrame(rows)


def load_quicksight_events():
    """Return DataFrame [login, product, month, views] for Axis Monthly and Cerberus."""
    raw = pd.read_excel(QS, sheet_name="sheet1", header=None)
    # Identify month columns (header on 1-indexed row 5, i.e., raw row 4)
    # Row 4 (raw index 4): month labels in col indexes 1,3,5,7,9,11,13,15,17
    # Row 5 (raw index 5): 'login_id', 'eventname' pairs
    month_cols = {}
    header_row_idx = 4  # 1-indexed row 5 -> 0-indexed row 4
    subhdr_row_idx = 5  # 1-indexed row 6 -> 0-indexed row 5; but col labels live at raw[4]
    # Actually per inspection: row index 4 has month labels (in pair columns), row 5 is 'login_id'/'eventname'
    for col in range(1, raw.shape[1]):
        label = raw.iloc[4, col]
        if isinstance(label, str) and " 20" in label:
            # this is a login_id column; eventname is next
            ts = pd.to_datetime(label, errors="coerce")
            if pd.isna(ts):
                continue
            m = ts.strftime("%Y-%m")
            month_cols[m] = (col, col + 1)

    axis_df = parse_quicksight_section(raw, "Axis Monthly",
                                       QS_AXIS_ROWS[0], QS_AXIS_ROWS[1], month_cols)
    cerb_df = parse_quicksight_section(raw, "Cerberus",
                                       QS_CERBERUS_ROWS[0], QS_CERBERUS_ROWS[1], month_cols)
    events = pd.concat([axis_df, cerb_df], ignore_index=True)
    # map dashboard -> product
    events["product"] = events["dashboard"].map({"Axis Monthly": "Axis", "Cerberus": "Cerberus"})
    return events


def tableau_product_for_dashboard(dash, keep):
    if dash not in keep:
        return None
    if "Yeti BOM" in dash:
        return "Yeti BOM"
    if dash == "Inventory Reporting":
        return "Inventory Reporting"
    return dash


def load_tableau_filter(path, sheet_name):
    df = pd.read_excel(path, sheet_name=sheet_name, header=None)
    return set(df.iloc[:, 0].dropna().tolist())


def load_tableau_unique_users_events(keep_set):
    df = pd.read_excel(TBU, sheet_name="Sheet 1", header=1)
    df[["Column1", "Column2", "Column3"]] = df[["Column1", "Column2", "Column3"]].ffill()
    # subtotal row has Column 4 = 'Total'
    df = df[df["Column 4"].notna() & (df["Column 4"] != "Total")].copy()
    df = df.rename(columns={"Column2": "Dashboard", "Column 4": "Viewer"})
    df["product"] = df["Dashboard"].apply(lambda d: tableau_product_for_dashboard(d, keep_set))
    df = df[df["product"].notna()].copy()
    meta = {"Column1", "Dashboard", "Column3", "Viewer", "Column 5", "Total", "product"}
    date_cols = [c for c in df.columns if c not in meta]
    long = df.melt(id_vars=["Viewer", "product"], value_vars=date_cols,
                   var_name="date_col", value_name="flag")
    long = long[long["flag"].fillna(0) > 0].copy()
    long["month"] = long["date_col"].apply(month_key)
    long = long.dropna(subset=["month"])
    return long[["Viewer", "product", "month", "flag"]].rename(columns={"Viewer": "login"})


def load_tableau_total_views_events(keep_set):
    df = pd.read_excel(TBV, sheet_name="Sheet 1", header=1)
    df[["Project", "Dashboard", "Owner"]] = df[["Project", "Dashboard", "Owner"]].ffill()
    df = df[df["Viewer"].notna() & (df["Viewer"] != "Total")].copy()
    df["product"] = df["Dashboard"].apply(lambda d: tableau_product_for_dashboard(d, keep_set))
    df = df[df["product"].notna()].copy()
    meta = {"Project", "Dashboard", "Owner", "Viewer", "Department", "Total", "product"}
    date_cols = [c for c in df.columns if c not in meta]
    long = df.melt(id_vars=["Viewer", "product"], value_vars=date_cols,
                   var_name="date_col", value_name="views")
    long = long[long["views"].fillna(0) > 0].copy()
    long["month"] = long["date_col"].apply(month_key)
    long = long.dropna(subset=["month"])
    return long[["Viewer", "product", "month", "views"]].rename(columns={"Viewer": "login"})


def build_dashboard_avenue(chain_map, qs_keep, tbu_keep, tbv_keep):
    """Aggregate per-manager per-product-month metrics from dashboard sources.
    QuickSight: full (distinct_users + total_views).
    Tableau UniqueUsers: distinct_users only.
    Tableau TotalViews: total_views only.
    Same product counted once per user per month per source.
    """
    qs_events = load_quicksight_events()
    qs_events = qs_events[qs_events["product"].notna()]
    # qs_events columns: login, product, month, views

    tbu = load_tableau_unique_users_events(tbu_keep)  # login, product, month, flag
    tbv = load_tableau_total_views_events(tbv_keep)  # login, product, month, views

    # Build per-(mgr, product, month) distinct users from QuickSight + TBU combined logins
    frames_users = []
    if not qs_events.empty:
        frames_users.append(qs_events[["login", "product", "month"]])
    if not tbu.empty:
        frames_users.append(tbu[["login", "product", "month"]])

    # Build per-(mgr, product, month) total_views from QuickSight + TBV
    # Use attribute_events logic for both

    # Distinct users: merge login sets then attribute
    user_frame = (pd.concat(frames_users, ignore_index=True) if frames_users
                  else pd.DataFrame(columns=["login", "product", "month"]))
    user_frame = user_frame.drop_duplicates()
    user_frame["views"] = 0  # placeholder; we'll pull from view frames

    # Views frame (two sources, summed)
    view_frames = []
    if not qs_events.empty:
        view_frames.append(qs_events[["login", "product", "month", "views"]])
    if not tbv.empty:
        view_frames.append(tbv[["login", "product", "month", "views"]])
    view_frame = (pd.concat(view_frames, ignore_index=True) if view_frames
                  else pd.DataFrame(columns=["login", "product", "month", "views"]))
    view_frame = view_frame.groupby(["login", "product", "month"])["views"].sum().reset_index()

    # Attribute each user to their manager chain and compute distinct counts and view sums
    # Use attribute_events separately and merge

    def attribute(df, views_col):
        rows = []
        for _, r in df.iterrows():
            chain = chain_map.get(r["login"])
            if not chain:
                continue
            views = r[views_col] if views_col else 0.0
            for mgr, _lvl in chain:
                rows.append({"manager_login": mgr, "product": r["product"],
                             "month": r["month"], "login": r["login"],
                             "views": float(views) if views_col else 0.0})
        return pd.DataFrame(rows) if rows else pd.DataFrame(
            columns=["manager_login", "product", "month", "login", "views"])

    user_attr = attribute(user_frame, views_col=None)
    view_attr = attribute(view_frame, views_col="views")

    du = (user_attr.groupby(["manager_login", "product", "month"])["login"]
          .nunique().reset_index(name="distinct_users"))
    tv = (view_attr.groupby(["manager_login", "product", "month"])["views"]
          .sum().reset_index(name="total_views"))

    out = du.merge(tv, on=["manager_login", "product", "month"], how="outer").fillna(0)
    out["distinct_users"] = out["distinct_users"].astype(int)
    out["total_views"] = out["total_views"].astype(float)
    out["avenue"] = AVENUE_DASH
    return out, qs_events, tbu, tbv


# -----------------------------------------------------------------------------
# Manager meta
# -----------------------------------------------------------------------------
def load_manager_meta():
    df = pd.read_excel(OP, sheet_name="Result 1")
    meta = df[["manager_login", "manager_name", "job_level_name", "team_size",
               "manager_hierarchy"]].drop_duplicates(subset=["manager_login"])
    meta["direct_mgr"] = meta["manager_hierarchy"].apply(direct_parent)
    return meta.set_index("manager_login")


# -----------------------------------------------------------------------------
# Build rows per (product, avenue)
# -----------------------------------------------------------------------------
def metrics_of(agg, login, product, avenue, months):
    sub = agg[(agg["manager_login"] == login)
              & (agg["product"] == product)
              & (agg["avenue"] == avenue)]
    out = {}
    for m in months:
        r = sub[sub["month"] == m]
        if r.empty:
            out[m] = (0, 0.0)
        else:
            out[m] = (int(r["distinct_users"].iloc[0]), float(r["total_views"].iloc[0]))
    return out


def has_data(metrics):
    return any(du > 0 or tv > 0 for du, tv in metrics.values())


def collect_rows_for_product_avenue(agg, meta, product, avenue, months, base_outline):
    """Return list of row dicts. base_outline is the outline level of the L11 row."""
    l11_meta = meta[meta["job_level_name"] == 11]
    l11_names = set(l11_meta["manager_name"])
    top_l11 = l11_meta[~l11_meta["direct_mgr"].isin(l11_names)]

    candidates = []
    for login, r in top_l11.iterrows():
        m = metrics_of(agg, login, product, avenue, months)
        if has_data(m):
            candidates.append((r["manager_name"], login, r["team_size"], m))
    candidates.sort(key=lambda x: x[0].lower())

    rows = []
    for name, login, tsize, m in candidates:
        rows.append(dict(level="L11", outline=base_outline, name=name, login=login,
                         team_size=tsize, metrics=m))
        # nested L11
        dir_l11 = meta[(meta["job_level_name"] == 11) & (meta["direct_mgr"] == name)]
        for c_login, cr in dir_l11.iterrows():
            cm = metrics_of(agg, c_login, product, avenue, months)
            if has_data(cm):
                rows.append(dict(level="L11", outline=base_outline + 1, name=cr["manager_name"],
                                 login=c_login, team_size=cr["team_size"], metrics=cm))
                dir_l10n = meta[(meta["job_level_name"] == 10) &
                                (meta["direct_mgr"] == cr["manager_name"])]
                for c10_login, c10 in dir_l10n.iterrows():
                    c10m = metrics_of(agg, c10_login, product, avenue, months)
                    if has_data(c10m):
                        rows.append(dict(level="L10", outline=base_outline + 2, name=c10["manager_name"],
                                         login=c10_login, team_size=c10["team_size"], metrics=c10m))
                        dir_any = meta[meta["direct_mgr"] == c10["manager_name"]]
                        dir_any = dir_any.sort_values(["job_level_name", "team_size"],
                                                      ascending=[False, False])
                        for d_login, dr in dir_any.iterrows():
                            dm = metrics_of(agg, d_login, product, avenue, months)
                            if has_data(dm):
                                rows.append(dict(level=f"L{int(dr['job_level_name'])}",
                                                 outline=base_outline + 3, name=dr["manager_name"],
                                                 login=d_login, team_size=dr["team_size"], metrics=dm))
        # direct L10
        dir_l10 = meta[(meta["job_level_name"] == 10) & (meta["direct_mgr"] == name)]
        for c_login, cr in dir_l10.iterrows():
            cm = metrics_of(agg, c_login, product, avenue, months)
            if has_data(cm):
                rows.append(dict(level="L10", outline=base_outline + 1, name=cr["manager_name"],
                                 login=c_login, team_size=cr["team_size"], metrics=cm))
                dir_any = meta[meta["direct_mgr"] == cr["manager_name"]]
                dir_any = dir_any.sort_values(["job_level_name", "team_size"],
                                              ascending=[False, False])
                for d_login, dr in dir_any.iterrows():
                    dm = metrics_of(agg, d_login, product, avenue, months)
                    if has_data(dm):
                        rows.append(dict(level=f"L{int(dr['job_level_name'])}",
                                         outline=base_outline + 2, name=dr["manager_name"],
                                         login=d_login, team_size=dr["team_size"], metrics=dm))
    return rows


def totals_of_rows(rows, target_outline, months):
    tot = {m: (0, 0.0) for m in months}
    for r in rows:
        if r["outline"] == target_outline:
            for m in months:
                du, tv = r["metrics"][m]
                tot[m] = (tot[m][0] + du, tot[m][1] + tv)
    return tot


# Colours (muted palette, same as existing sheet)
FILL_PRODUCT = PatternFill("solid", fgColor="4F6D7A")
FILL_AVENUE = PatternFill("solid", fgColor="B5C7C7")
FILL_L1 = PatternFill("solid", fgColor="D8E2DC")
FILL_L2 = PatternFill("solid", fgColor="ECE4DB")
FILL_L3 = PatternFill("solid", fgColor="F8F5F2")
FILL_L4 = PatternFill("solid", fgColor="FFFFFF")
FILL_HEADER = PatternFill("solid", fgColor="4F6D7A")


def write_sheet(wb, agg, meta, months, product_avenues):
    if SHEET in wb.sheetnames:
        del wb[SHEET]
    ws = wb.create_sheet(SHEET)

    header1 = ["Leader / Product", "Level", "Team Size", "Entitled Users", "Login"]
    for m in months:
        header1.extend([m, ""])
    header2 = ["", "", "", "", ""]
    for _ in months:
        header2.extend(["Distinct Users", "Total Views"])
    ws.append(header1)
    ws.append(header2)
    for i in range(len(months)):
        start = 6 + i * 2
        ws.merge_cells(start_row=1, end_row=1, start_column=start, end_column=start + 1)

    header_font = Font(bold=True, color="FFFFFF")
    center = Alignment(horizontal="center", vertical="center")
    for col in range(1, len(header2) + 1):
        for row in (1, 2):
            c = ws.cell(row=row, column=col)
            c.font = header_font
            c.fill = FILL_HEADER
            c.alignment = center

    ws.sheet_properties.outlinePr.summaryBelow = False
    ws.sheet_properties.outlinePr.summaryRight = False
    ws.sheet_format.outlineLevelRow = 0

    fill_by_outline = {0: FILL_PRODUCT, 1: FILL_AVENUE, 2: FILL_L1, 3: FILL_L2, 4: FILL_L3, 5: FILL_L4}
    font_by_outline = {
        0: Font(bold=True, color="FFFFFF"),
        1: Font(bold=True, color="2F4858"),
        2: Font(bold=True, color="2F4858"),
        3: Font(bold=False),
        4: Font(bold=False),
        5: Font(bold=False, color="666666"),
    }

    current_row = 3
    products = sorted(product_avenues.keys(), key=str.lower)

    for product in products:
        avenues = product_avenues[product]  # list
        # Product row totals = sum across avenues of avenue L11 totals
        product_tot = {m: (0, 0.0) for m in months}

        # Pre-compute avenue row sets and totals
        avenue_blocks = []
        for avenue in avenues:
            base_outline = 2 if len(avenues) > 1 else 1
            prod_rows = collect_rows_for_product_avenue(agg, meta, product, avenue, months, base_outline)
            if not prod_rows:
                continue
            av_tot = totals_of_rows(prod_rows, base_outline, months)
            avenue_blocks.append((avenue, prod_rows, av_tot, base_outline))
            for m in months:
                product_tot[m] = (product_tot[m][0] + av_tot[m][0], product_tot[m][1] + av_tot[m][1])

        if not avenue_blocks:
            continue

        # Product row
        rv = [product, "Product", None, None, None]
        for m in months:
            du, tv = product_tot[m]
            rv.extend([du, round(tv, 2)])
        ws.append(rv)
        for col in range(1, len(rv) + 1):
            c = ws.cell(row=current_row, column=col)
            c.font = font_by_outline[0]
            c.fill = fill_by_outline[0]
        current_row += 1

        has_multiple = len(avenue_blocks) > 1
        for avenue, prod_rows, av_tot, base_outline in avenue_blocks:
            if has_multiple:
                rv = [f"  [{avenue}]", "Avenue", None, None, None]
                for m in months:
                    du, tv = av_tot[m]
                    rv.extend([du, round(tv, 2)])
                ws.append(rv)
                ws.row_dimensions[current_row].outline_level = 1
                ws.row_dimensions[current_row].hidden = True
                for col in range(1, len(rv) + 1):
                    c = ws.cell(row=current_row, column=col)
                    c.font = font_by_outline[1]
                    c.fill = fill_by_outline[1]
                current_row += 1

            for r in prod_rows:
                indent = "    " * (r["outline"] - (1 if has_multiple else 0))
                data = [indent + r["name"], r["level"], r["team_size"], None, r["login"]]
                for m in months:
                    du, tv = r["metrics"][m]
                    data.extend([du, round(tv, 2)])
                ws.append(data)
                ws.row_dimensions[current_row].outline_level = r["outline"]
                ws.row_dimensions[current_row].hidden = True
                fill = fill_by_outline.get(r["outline"], FILL_L4)
                font = font_by_outline.get(r["outline"], Font())
                for col in range(1, len(data) + 1):
                    c = ws.cell(row=current_row, column=col)
                    c.font = font
                    c.fill = fill
                current_row += 1

    ws.freeze_panes = "F3"
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 11
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 12
    for i in range(len(months)):
        ws.column_dimensions[get_column_letter(6 + i * 2)].width = 14
        ws.column_dimensions[get_column_letter(7 + i * 2)].width = 12


# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------
def validate(agg, months):
    wb = load_workbook(OP)
    ws = wb[SHEET]
    month_cols = {m: (6 + i * 2, 7 + i * 2) for i, m in enumerate(months)}

    # Pre-build: for each product, which avenues are present. Single-avenue products
    # don't display an Avenue row, so we need to remember the sole avenue.
    prod_avs = agg.groupby("product")["avenue"].unique().apply(list).to_dict()

    checks = 0
    mismatches = 0
    product_ctx = None
    avenue_ctx = None
    for row in range(3, ws.max_row + 1):
        level_val = ws.cell(row=row, column=2).value
        login = ws.cell(row=row, column=5).value
        name_raw = ws.cell(row=row, column=1).value or ""
        if level_val == "Product":
            product_ctx = name_raw.strip()
            avs = prod_avs.get(product_ctx, [])
            avenue_ctx = avs[0] if len(avs) == 1 else None
            continue
        if level_val == "Avenue":
            avenue_ctx = name_raw.strip().strip("[]").strip()
            continue
        if not login or avenue_ctx is None:
            continue
        sub = agg[(agg["manager_login"] == login)
                  & (agg["product"] == product_ctx)
                  & (agg["avenue"] == avenue_ctx)]
        for m, (cdu, ctv) in month_cols.items():
            r = sub[sub["month"] == m]
            exp_du = int(r["distinct_users"].iloc[0]) if not r.empty else 0
            exp_tv = float(r["total_views"].iloc[0]) if not r.empty else 0.0
            got_du = ws.cell(row=row, column=cdu).value or 0
            got_tv = ws.cell(row=row, column=ctv).value or 0
            checks += 2
            if int(got_du) != exp_du:
                mismatches += 1
                if mismatches <= 15:
                    print(f"  MISMATCH DU row={row} [{product_ctx}|{avenue_ctx}|{login}|{m}]: got {got_du} vs {exp_du}")
            if abs(float(got_tv) - exp_tv) > 0.01:
                mismatches += 1
                if mismatches <= 15:
                    print(f"  MISMATCH TV row={row} [{product_ctx}|{avenue_ctx}|{login}|{m}]: got {got_tv} vs {exp_tv}")
    print(f"\nValidation: {checks} cells checked, {mismatches} mismatches")
    return checks, mismatches


# -----------------------------------------------------------------------------
# QuickSight dashboard totals cross-check
# -----------------------------------------------------------------------------
def crosscheck_quicksight(qs_events):
    """Compare parsed user-row totals + NaN-row unattributed events to dashboard header."""
    raw = pd.read_excel(QS, sheet_name="sheet1", header=None)
    # Dashboard header rows (0-indexed): Axis Monthly = 7, Cerberus = 102
    # NaN-row (unattributed) immediately after: 8 and 103
    dashboards = {"Axis Monthly": (7, 8), "Cerberus": (102, 103)}
    month_cols = {}
    for col in range(1, raw.shape[1]):
        label = raw.iloc[4, col]
        if isinstance(label, str) and " 20" in label:
            ts = pd.to_datetime(label, errors="coerce")
            if pd.notna(ts):
                month_cols[ts.strftime("%Y-%m")] = (col, col + 1)

    print("\nQuickSight parsed vs source dashboard-header totals (including NaN-row unattributed):")
    ok = True
    for dash, (hdr_idx, nan_idx) in dashboards.items():
        dash_events = qs_events[qs_events["dashboard"] == dash]
        for m, (li_col, en_col) in month_cols.items():
            src_du = 0 if pd.isna(raw.iloc[hdr_idx, li_col]) else int(raw.iloc[hdr_idx, li_col])
            src_tv = 0 if pd.isna(raw.iloc[hdr_idx, en_col]) else float(raw.iloc[hdr_idx, en_col])
            nan_tv = 0 if pd.isna(raw.iloc[nan_idx, en_col]) else float(raw.iloc[nan_idx, en_col])
            mine = dash_events[dash_events["month"] == m]
            mine_du = mine["login"].nunique()
            mine_tv = mine["views"].sum()
            # Our parsed TV should equal src_tv - nan_tv (we exclude unattributed events)
            exp_tv = src_tv - nan_tv
            if mine_du != src_du or abs(mine_tv - exp_tv) > 0.01:
                ok = False
                print(f"  {dash} {m}: parsed DU={mine_du} TV={mine_tv} vs src DU={src_du} TV-nan={exp_tv} (src={src_tv}, nan={nan_tv})")
    if ok:
        print("  all months tie for Axis Monthly and Cerberus (parsed = source dashboard total minus unattributed NaN-row events).")


# -----------------------------------------------------------------------------
# Consolidated users sheet
# -----------------------------------------------------------------------------
def write_consolidated_users(chain_map, qs_events, tbu_long, tbv_long):
    logins = set()
    for s in [qs_events, tbu_long, tbv_long]:
        if s is not None and not s.empty:
            logins.update(s["login"].dropna().unique())

    # Build employee_name lookup (chain[0] is the user themselves)
    hier_df = pd.read_excel(HIER, sheet_name="Result 1")
    login_to_name = dict(zip(hier_df["login_name"], hier_df["employee_name"]))

    rows = []
    for login in sorted(logins):
        in_qs = not qs_events.empty and login in set(qs_events["login"])
        in_tbu = not tbu_long.empty and login in set(tbu_long["login"])
        in_tbv = not tbv_long.empty and login in set(tbv_long["login"])
        in_hier = login in chain_map
        rows.append({
            "login": login,
            "employee_name": login_to_name.get(login, ""),
            "in_hierarchy": "Yes" if in_hier else "No",
            "in_quicksight": "Yes" if in_qs else "No",
            "in_tableau_unique_users": "Yes" if in_tbu else "No",
            "in_tableau_total_views": "Yes" if in_tbv else "No",
        })
    df = pd.DataFrame(rows)

    wb = load_workbook(QS)
    sn = "consolidated users"
    if sn in wb.sheetnames:
        del wb[sn]
    ws = wb.create_sheet(sn)
    ws.append(list(df.columns))
    for _, r in df.iterrows():
        ws.append(r.tolist())
    for col_idx, col in enumerate(df.columns, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = max(18, len(col) + 2)
        ws.cell(row=1, column=col_idx).font = Font(bold=True, color="FFFFFF")
        ws.cell(row=1, column=col_idx).fill = FILL_HEADER
    wb.save(QS)
    print(f"\nWrote 'consolidated users' sheet with {len(df)} logins to {os.path.basename(QS)}")
    return df


def main():
    print("Loading hierarchy ...")
    chain_map = load_hierarchy()

    print("Loading op_excellence ...")
    op_agg = load_op_excellence()
    # Product map identity; v1 already has 'Inventory Reporting'
    print(f"  {len(op_agg)} rows; products={sorted(op_agg['product'].unique())}")

    print("Loading dashboard-avenue sources ...")
    tbu_keep = load_tableau_filter(TBU, "Filtered Dashboards")
    tbv_keep = load_tableau_filter(TBV, "Dasboards")
    dash_agg, qs_events, tbu_long, tbv_long = build_dashboard_avenue(chain_map, None, tbu_keep, tbv_keep)
    print(f"  {len(dash_agg)} rows; products={sorted(dash_agg['product'].unique())}")

    # Combine
    agg = pd.concat([op_agg, dash_agg], ignore_index=True)
    print(f"Combined: {len(agg)} rows")

    # Determine avenues per product
    product_avenues = {}
    for product in sorted(agg["product"].unique()):
        avs = []
        if ((agg["product"] == product) & (agg["avenue"] == AVENUE_OP)).any():
            avs.append(AVENUE_OP)
        if ((agg["product"] == product) & (agg["avenue"] == AVENUE_DASH)).any():
            avs.append(AVENUE_DASH)
        product_avenues[product] = avs
    print("\nAvenues per product:")
    for p, avs in product_avenues.items():
        print(f"  {p}: {avs}")

    meta = load_manager_meta()
    months = sorted(agg["month"].dropna().unique(), reverse=True)
    print(f"\nMonths: {months}")

    print("\nCross-checking QuickSight user-row sums vs source totals ...")
    crosscheck_quicksight(qs_events)

    print("\nWriting main sheet ...")
    wb = load_workbook(OP)
    write_sheet(wb, agg, meta, months, product_avenues)
    wb.save(OP)

    print("\nValidating every row ...")
    validate(agg, months)

    print("\nBuilding 'consolidated users' sheet ...")
    write_consolidated_users(chain_map, qs_events, tbu_long, tbv_long)


if __name__ == "__main__":
    main()
