"""
Build the integrated Product x L11 rollup that combines
- op_excellence (the per-manager source of truth)
- QuickSight raw events (via hierarchy map to L11/L10)
- Tableau viewership (via hierarchy map to L11/L10), restricted to 13 dashboards

Option C merging: per (product, leader, month), sum op_excellence + new-source metrics.

Product consolidation rules:
- Axis           = op_excellence 'Axis' + QuickSight 'Axis Monthly'
- Inventory Reporting = op_excellence 'Inventory Reporting' + Tableau dashboard 'Inventory Reporting'
- Yeti BOM       = op_excellence 'Yeti BOM' + Tableau dashboards containing 'Yeti BOM'
- Cerberus       = QuickSight 'Cerberus' (new product)
- Other Tableau dashboards in the 'Dasboards' filter = each becomes its own product

Output: overwrite sheet 'Product Rollup by L11' in the op_excellence workbook.
"""
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = "/Users/propatil/Desktop/Other Projects/TPM_Related/Products Usage Metrics/Excel Analysis"
OP_XLSX = os.path.join(BASE, "usage metrics op_excellence_20260415.xlsx")
QS_XLSX = os.path.join(BASE, "QuickSight UniqueUsers&TotalView_ExcludingFinTech_20260420.xlsx")
TB_UV_XLSX = os.path.join(BASE, "Tableau Unique Viewers_Crosstab_ExclFinTech_20260420.xlsx")
TB_TV_XLSX = os.path.join(BASE, "Tableau TotalViews_ExclFinTech_20260420.xlsx")
HIER_XLSX = os.path.join(BASE, "das_finops_op_excellmployee_hierarchy_all.xlsx")

SHEET_NAME = "Product Rollup by L11"


def month_of(d):
    ts = pd.to_datetime(d, errors="coerce")
    return None if pd.isna(ts) else ts.strftime("%Y-%m")


def direct_parent(h):
    if not isinstance(h, str):
        return None
    parts = h.split(":")
    return parts[1] if len(parts) > 1 else None


# -----------------------------------------------------------------------------
# Hierarchy map: login_id -> list of ancestor logins (each level)
# -----------------------------------------------------------------------------
def load_hierarchy():
    h = pd.read_excel(HIER_XLSX, sheet_name="Result 1")
    h = h.dropna(subset=["login_name", "manager_login_hierarchy_concat"]).copy()
    # Parse the concat columns to a list of (login, level) pairs from self up
    h["chain_logins"] = h["manager_login_hierarchy_concat"].str.split(":")
    h["chain_levels"] = h["manager_job_level_hierarchy_concat"].astype(str).str.split(":")

    def build_chain(row):
        logins = row["chain_logins"]
        levels = row["chain_levels"]
        # Chain includes self at index 0; levels list length matches
        if len(logins) != len(levels):
            return []
        return list(zip(logins, [int(x) if x.isdigit() else None for x in levels]))

    h["chain"] = h.apply(build_chain, axis=1)
    return h.set_index("login_name")["chain"].to_dict()


# -----------------------------------------------------------------------------
# Usage event enrichment: each usage event is attributed to EVERY ancestor
# manager in the user's chain. This way a manager row reflects "activity
# anywhere in my org". This matches how op_excellence rolls up.
# -----------------------------------------------------------------------------
def attribute_events_to_managers(events_df, login_to_chain, login_col,
                                  product_col, month_col, views_col=None):
    """
    events_df: one row per event (or aggregated per user-period).
    views_col: if None, each row counts as 1 view. If set, sum that column.
    login_col, product_col, month_col: column names in events_df.

    Returns DataFrame with columns:
        manager_login, product, month, distinct_users, total_views
    - distinct_users: count distinct logins in the subtree that used product
      in the month. Computed at manager level.
    - total_views: sum of views credited to that manager's subtree.
    """
    rows = []
    for _, r in events_df.iterrows():
        login = r[login_col]
        product = r[product_col]
        month = r[month_col]
        views = 1 if views_col is None else (
            r[views_col] if pd.notna(r[views_col]) else 0
        )
        chain = login_to_chain.get(login)
        if not chain:
            continue
        for mgr_login, mgr_level in chain:
            rows.append(
                {
                    "manager_login": mgr_login,
                    "manager_level": mgr_level,
                    "product": product,
                    "month": month,
                    "login": login,  # for distinct count
                    "views": views,
                }
            )
    if not rows:
        return pd.DataFrame(columns=["manager_login", "product", "month",
                                     "distinct_users", "total_views"])
    df = pd.DataFrame(rows)
    g = df.groupby(["manager_login", "product", "month"]).agg(
        distinct_users=("login", "nunique"),
        total_views=("views", "sum"),
    ).reset_index()
    return g


# -----------------------------------------------------------------------------
# Load each source and produce a unified events frame
# -----------------------------------------------------------------------------
def load_op_excellence():
    df = pd.read_excel(OP_XLSX, sheet_name="Result 1")
    df["month"] = df["log_week"].apply(month_of)
    df = df[df["application_type"].notna()]
    # per-manager monthly sum already available directly
    agg = df.groupby(["manager_login", "application_type", "month"]).agg(
        distinct_users=("distinct_users", "sum"),
        total_views=("total_measure_value", "sum"),
    ).reset_index()
    agg = agg.rename(columns={"application_type": "product"})
    return agg


def load_quicksight(login_to_chain):
    qs = pd.read_excel(QS_XLSX, sheet_name="sheet1", header=2)
    qs = qs[qs["login_id"].notna() & qs["Dashboard Name"].notna() & qs["eventtime"].notna()].copy()
    qs["month"] = qs["eventtime"].apply(month_of)
    # Product mapping: 'Axis Monthly' -> 'Axis', other -> dashboard name
    qs["product"] = qs["Dashboard Name"].where(qs["Dashboard Name"] != "Axis Monthly", "Axis")
    # Each event is one view
    return attribute_events_to_managers(
        qs, login_to_chain,
        login_col="login_id", product_col="product", month_col="month",
        views_col=None,  # each event = 1 view
    )


def tableau_product_for_dashboard(dashboard, keep_set):
    """Map dashboard name -> unified product. Only return for dashboards in keep_set."""
    if dashboard not in keep_set:
        return None
    if "Yeti BOM" in dashboard:
        return "Yeti BOM"
    if dashboard == "Inventory Reporting":
        return "Inventory Reporting"
    return dashboard  # standalone product


def load_tableau_dashboards_filter():
    df = pd.read_excel(TB_TV_XLSX, sheet_name="Dasboards", header=None)
    return set(df.iloc[:, 0].dropna().tolist())


def load_tableau_unique_viewers(login_to_chain, keep_set):
    uv = pd.read_excel(TB_UV_XLSX, sheet_name="Sheet 1", header=1)
    uv[["Project", "Dashboard", "Owner"]] = uv[["Project", "Dashboard", "Owner"]].ffill()
    uv = uv[~((uv["Viewer"].astype(str) == "Total") & (uv["Department"].astype(str) == "Total"))]
    uv = uv[uv["Viewer"].notna()].copy()
    uv["product"] = uv["Dashboard"].apply(lambda d: tableau_product_for_dashboard(d, keep_set))
    uv = uv[uv["product"].notna()].copy()

    # Melt weekly date columns. Each non-null numeric value = that viewer was
    # active that week (count is the weekly user-count, typically 1 for Tableau).
    meta_cols = ["Project", "Dashboard", "Owner", "Viewer", "Department", "Unnamed: 5", "product"]
    date_cols = [c for c in uv.columns if c not in meta_cols]

    long = uv.melt(id_vars=["Viewer", "product"], value_vars=date_cols,
                   var_name="week", value_name="cnt")
    long = long[long["cnt"].fillna(0) > 0].copy()
    long["month"] = long["week"].apply(month_of)
    long = long.dropna(subset=["month"])

    # Unique viewers: per (product, month), count distinct Viewer in manager subtree.
    # attribute_events_to_managers handles this, with views_col=None giving 1 view
    # per viewer-week row. We pass "cnt" as views_col to get real view counts.
    # BUT: this is the UNIQUE VIEWERS file - weekly counts are typically 1 and
    # don't represent actual view totals. We'll use it ONLY for distinct_users.
    # total_views handled by TotalViews file.
    return attribute_events_to_managers(
        long, login_to_chain,
        login_col="Viewer", product_col="product", month_col="month",
        views_col=None,
    )[["manager_login", "product", "month", "distinct_users"]]  # views discarded


def load_tableau_total_views(login_to_chain, keep_set):
    tv = pd.read_excel(TB_TV_XLSX, sheet_name="Sheet 1", header=1)
    tv[["Project", "Dashboard", "Owner"]] = tv[["Project", "Dashboard", "Owner"]].ffill()
    tv = tv[tv["Viewer"].notna() & tv["Dashboard"].notna()].copy()
    tv["product"] = tv["Dashboard"].apply(lambda d: tableau_product_for_dashboard(d, keep_set))
    tv = tv[tv["product"].notna()].copy()

    meta_cols = ["Project", "Dashboard", "Owner", "Viewer", "Department", "Total", "product"]
    date_cols = [c for c in tv.columns if c not in meta_cols]

    long = tv.melt(id_vars=["Viewer", "product"], value_vars=date_cols,
                   var_name="month_col", value_name="views")
    long = long[long["views"].fillna(0) > 0].copy()
    long["month"] = long["month_col"].apply(month_of)
    long = long.dropna(subset=["month"])

    # views_col carries actual monthly view counts
    out = attribute_events_to_managers(
        long, login_to_chain,
        login_col="Viewer", product_col="product", month_col="month",
        views_col="views",
    )
    # Only keep total_views from this file
    return out[["manager_login", "product", "month", "total_views"]]


def combine_sources(op, qs, tb_uv, tb_tv):
    """Sum all four sources on (manager_login, product, month)."""
    frames = []
    if not op.empty:
        frames.append(op)
    if not qs.empty:
        frames.append(qs)
    if not tb_uv.empty:
        t = tb_uv.copy()
        t["total_views"] = 0
        frames.append(t)
    if not tb_tv.empty:
        t = tb_tv.copy()
        t["distinct_users"] = 0
        frames.append(t)
    merged = pd.concat(frames, ignore_index=True, sort=False).fillna(0)
    final = merged.groupby(["manager_login", "product", "month"]).agg(
        distinct_users=("distinct_users", "sum"),
        total_views=("total_views", "sum"),
    ).reset_index()
    return final


# -----------------------------------------------------------------------------
# Manager metadata (from op_excellence, which has team_size and hierarchy)
# -----------------------------------------------------------------------------
def load_manager_meta():
    df = pd.read_excel(OP_XLSX, sheet_name="Result 1")
    meta = df[["manager_login", "manager_name", "job_level_name", "team_size",
               "manager_hierarchy"]].drop_duplicates(subset=["manager_login"])
    meta["direct_mgr"] = meta["manager_hierarchy"].apply(direct_parent)
    return meta.set_index("manager_login")


# -----------------------------------------------------------------------------
# Build display rows per product
# -----------------------------------------------------------------------------
def metrics_dict(agg, manager_login, product, months):
    sub = agg[(agg["manager_login"] == manager_login) & (agg["product"] == product)]
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


def collect_rows_for_product(agg, meta, product, months):
    l11_meta = meta[meta["job_level_name"] == 11]
    l11_names_set = set(l11_meta["manager_name"])
    top_l11 = l11_meta[~l11_meta["direct_mgr"].isin(l11_names_set)]

    l11_candidates = []
    for login, r in top_l11.iterrows():
        m = metrics_dict(agg, login, product, months)
        if has_data(m):
            l11_candidates.append((r["manager_name"], login, r["team_size"], m))
    l11_candidates.sort(key=lambda x: x[0].lower())

    rows = []
    for name, login, tsize, m in l11_candidates:
        rows.append(dict(level="L11", outline=1, name=name, login=login,
                         team_size=tsize, metrics=m))

        # nested L11 under this L11
        dir_l11 = meta[(meta["job_level_name"] == 11) & (meta["direct_mgr"] == name)]
        for c_login, cr in dir_l11.iterrows():
            cm = metrics_dict(agg, c_login, product, months)
            if has_data(cm):
                rows.append(dict(level="L11", outline=2, name=cr["manager_name"],
                                 login=c_login, team_size=cr["team_size"], metrics=cm))
                # L10s under that nested L11
                dir_l10_nested = meta[(meta["job_level_name"] == 10) &
                                      (meta["direct_mgr"] == cr["manager_name"])]
                for c10_login, c10 in dir_l10_nested.iterrows():
                    c10m = metrics_dict(agg, c10_login, product, months)
                    if has_data(c10m):
                        rows.append(dict(level="L10", outline=3, name=c10["manager_name"],
                                         login=c10_login, team_size=c10["team_size"],
                                         metrics=c10m))
                        dir_any = meta[meta["direct_mgr"] == c10["manager_name"]]
                        dir_any = dir_any.sort_values(
                            ["job_level_name", "team_size"], ascending=[False, False]
                        )
                        for d_login, dr in dir_any.iterrows():
                            dm = metrics_dict(agg, d_login, product, months)
                            if has_data(dm):
                                rows.append(dict(
                                    level=f"L{int(dr['job_level_name'])}",
                                    outline=4, name=dr["manager_name"], login=d_login,
                                    team_size=dr["team_size"], metrics=dm,
                                ))

        # direct L10 reports of parent L11
        dir_l10 = meta[(meta["job_level_name"] == 10) & (meta["direct_mgr"] == name)]
        for c_login, cr in dir_l10.iterrows():
            cm = metrics_dict(agg, c_login, product, months)
            if has_data(cm):
                rows.append(dict(level="L10", outline=2, name=cr["manager_name"],
                                 login=c_login, team_size=cr["team_size"], metrics=cm))
                dir_any = meta[meta["direct_mgr"] == cr["manager_name"]]
                dir_any = dir_any.sort_values(
                    ["job_level_name", "team_size"], ascending=[False, False]
                )
                for d_login, dr in dir_any.iterrows():
                    dm = metrics_dict(agg, d_login, product, months)
                    if has_data(dm):
                        rows.append(dict(
                            level=f"L{int(dr['job_level_name'])}",
                            outline=3, name=dr["manager_name"], login=d_login,
                            team_size=dr["team_size"], metrics=dm,
                        ))
    return rows


def product_totals(rows, months):
    """Product row = sum of outline=1 rows across months (no overlap between
    top-level L11 subtrees since they're disjoint Andy-Jassy-direct orgs)."""
    total = {m: (0, 0.0) for m in months}
    for r in rows:
        if r["outline"] == 1:
            for m in months:
                du, tv = r["metrics"][m]
                total[m] = (total[m][0] + du, total[m][1] + tv)
    return total


# -----------------------------------------------------------------------------
# Write the sheet
# -----------------------------------------------------------------------------
# Softer color palette
FILL_PRODUCT = PatternFill("solid", fgColor="4F6D7A")  # muted teal-grey
FILL_L1 = PatternFill("solid", fgColor="D8E2DC")       # soft sage
FILL_L2 = PatternFill("solid", fgColor="ECE4DB")       # warm cream
FILL_L3 = PatternFill("solid", fgColor="F8F5F2")       # off-white
FILL_L4 = PatternFill("solid", fgColor="FFFFFF")
FILL_HEADER = PatternFill("solid", fgColor="4F6D7A")


def write_sheet(wb, agg, meta, months):
    if SHEET_NAME in wb.sheetnames:
        del wb[SHEET_NAME]
    ws = wb.create_sheet(SHEET_NAME)

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

    level_fill = {0: FILL_PRODUCT, 1: FILL_L1, 2: FILL_L2, 3: FILL_L3, 4: FILL_L4}
    level_font = {
        0: Font(bold=True, color="FFFFFF"),
        1: Font(bold=True, color="2F4858"),
        2: Font(bold=False),
        3: Font(bold=False),
        4: Font(bold=False, color="666666"),
    }

    products = sorted(agg["product"].dropna().unique(), key=str.lower)
    current_row = 3

    for product in products:
        print(f"  Building: {product}")
        prod_rows = collect_rows_for_product(agg, meta, product, months)
        if not prod_rows:
            continue
        totals = product_totals(prod_rows, months)
        # Product header row
        row_vals = [product, "Product", None, None, None]
        for m in months:
            du, tv = totals[m]
            row_vals.extend([du, round(tv, 2)])
        ws.append(row_vals)
        for col in range(1, len(row_vals) + 1):
            c = ws.cell(row=current_row, column=col)
            c.font = level_font[0]
            c.fill = level_fill[0]
        current_row += 1

        for r in prod_rows:
            indent = "    " * (r["outline"] - 1)
            data = [indent + r["name"], r["level"], r["team_size"], None, r["login"]]
            for m in months:
                du, tv = r["metrics"][m]
                data.extend([du, round(tv, 2)])
            ws.append(data)
            ws.row_dimensions[current_row].outline_level = r["outline"]
            ws.row_dimensions[current_row].hidden = True
            for col in range(1, len(data) + 1):
                c = ws.cell(row=current_row, column=col)
                c.font = level_font[r["outline"]]
                c.fill = level_fill[r["outline"]]
            current_row += 1

    ws.freeze_panes = "F3"
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 8
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
    wb = load_workbook(OP_XLSX)
    ws = wb[SHEET_NAME]
    month_cols = {m: (6 + i * 2, 7 + i * 2) for i, m in enumerate(months)}

    checks = 0
    mismatches = 0
    product_ctx = None
    # Track top-level (outline=1) rows for product-total reconciliation
    product_l11_sums = {}  # product -> {month -> [du, tv]}

    for row in range(3, ws.max_row + 1):
        level_val = ws.cell(row=row, column=2).value
        login = ws.cell(row=row, column=5).value
        outline = ws.row_dimensions[row].outline_level or 0

        if level_val == "Product":
            product_ctx = (ws.cell(row=row, column=1).value or "").strip()
            product_l11_sums.setdefault(product_ctx, {m: [0, 0.0] for m in months})
            continue

        if not login:
            continue
        sub = agg[(agg["manager_login"] == login) & (agg["product"] == product_ctx)]
        for m, (cdu, ctv) in month_cols.items():
            r = sub[sub["month"] == m]
            exp_du = int(r["distinct_users"].iloc[0]) if not r.empty else 0
            exp_tv = float(r["total_views"].iloc[0]) if not r.empty else 0.0
            got_du = ws.cell(row=row, column=cdu).value or 0
            got_tv = ws.cell(row=row, column=ctv).value or 0
            checks += 2
            if int(got_du) != exp_du:
                mismatches += 1
                if mismatches <= 10:
                    print(f"  MISMATCH DU row={row} [{product_ctx}|{login}|{m}]: {got_du} vs {exp_du}")
            if abs(float(got_tv) - exp_tv) > 0.01:
                mismatches += 1
                if mismatches <= 10:
                    print(f"  MISMATCH TV row={row} [{product_ctx}|{login}|{m}]: {got_tv} vs {exp_tv}")
            if outline == 1:
                product_l11_sums[product_ctx][m][0] += int(got_du)
                product_l11_sums[product_ctx][m][1] += float(got_tv)

    # Check product row totals vs sum-of-L11s
    print("\nProduct-row vs sum-of-L11 reconciliation:")
    for row in range(3, ws.max_row + 1):
        level_val = ws.cell(row=row, column=2).value
        if level_val != "Product":
            continue
        product = (ws.cell(row=row, column=1).value or "").strip()
        for m, (cdu, ctv) in month_cols.items():
            prod_du = ws.cell(row=row, column=cdu).value or 0
            prod_tv = ws.cell(row=row, column=ctv).value or 0
            exp_du, exp_tv = product_l11_sums[product][m]
            if int(prod_du) != int(exp_du) or abs(float(prod_tv) - exp_tv) > 0.01:
                print(f"  [{product}|{m}] product row=({prod_du},{prod_tv}) vs sum-L11=({exp_du},{exp_tv})")

    print(f"\nValidation: {checks} cells, {mismatches} mismatches")


def main():
    print("Loading hierarchy map...")
    login_to_chain = load_hierarchy()

    print("Loading op_excellence...")
    op = load_op_excellence()
    print(f"  {len(op)} (mgr,product,month) rows")

    print("Loading QuickSight...")
    qs = load_quicksight(login_to_chain)
    print(f"  {len(qs)} (mgr,product,month) rows")

    print("Loading Tableau dashboard filter...")
    keep_set = load_tableau_dashboards_filter()
    print(f"  {len(keep_set)} dashboards kept: {sorted(keep_set)}")

    print("Loading Tableau Unique Viewers...")
    tb_uv = load_tableau_unique_viewers(login_to_chain, keep_set)
    print(f"  {len(tb_uv)} (mgr,product,month) rows")

    print("Loading Tableau Total Views...")
    tb_tv = load_tableau_total_views(login_to_chain, keep_set)
    print(f"  {len(tb_tv)} (mgr,product,month) rows")

    print("Combining sources (Option C)...")
    agg = combine_sources(op, qs, tb_uv, tb_tv)
    print(f"  final: {len(agg)} rows; products: {sorted(agg['product'].unique())}")

    print("Loading manager meta...")
    meta = load_manager_meta()

    months = sorted(agg["month"].dropna().unique(), reverse=True)
    print(f"Months: {months}")

    print("\nWriting sheet...")
    wb = load_workbook(OP_XLSX)
    write_sheet(wb, agg, meta, months)
    wb.save(OP_XLSX)
    print("Saved.\n")

    validate(agg, months)


if __name__ == "__main__":
    main()
