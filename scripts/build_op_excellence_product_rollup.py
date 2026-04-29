"""
Build a Product x L11 rollup sheet with collapsible hierarchy.

Hierarchy (Excel outline levels):
    0  Product family (application_type)
    1    L11 leader (direct reports of Andy Jassy who have data for the product)
    2      Direct L11 or L10 reports of the L11 (with data for the product)
    3        Direct L8 reports of the L10 (with data for the product)

Rules:
- Each row uses that manager's OWN rollup row from the source sheet. Parents
  are never computed by summing children, so no double counting occurs when
  an L11 reports through another L11.
- "Direct" means parent appears at index 1 of manager_hierarchy (split by ':').
- Only rows that have non-zero data for the product in at least one month
  are included.
- Depth is capped at L10's direct L8 reports.

Layout columns:
    A Leader (indented by outline level)
    B Level
    C Team Size
    D Entitled Users (blank)
    E+ per month, desc: <YYYY-MM> Distinct Users | <YYYY-MM> Total Views
"""
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE = "/Users/propatil/Desktop/Other Projects/TPM_Related/Products Usage Metrics/Excel Analysis"
SRC = os.path.join(BASE, "usage metrics op_excellence_20260415.xlsx")


def month_of(d):
    ts = pd.to_datetime(d, errors="coerce")
    return None if pd.isna(ts) else ts.strftime("%Y-%m")


def load_source():
    df = pd.read_excel(SRC, sheet_name="Result 1")
    df["month"] = df["log_week"].apply(month_of)
    return df


def direct_parent(hier):
    if not isinstance(hier, str):
        return None
    parts = hier.split(":")
    return parts[1] if len(parts) > 1 else None


def monthly_agg(sub_df, months):
    """Return dict month -> (distinct_users_sum, total_views_sum). Missing months become zero."""
    if sub_df.empty:
        return {m: (0, 0.0) for m in months}
    g = sub_df.groupby("month").agg(
        du=("distinct_users", "sum"),
        tv=("total_measure_value", "sum"),
    )
    out = {}
    for m in months:
        if m in g.index:
            out[m] = (int(g.loc[m, "du"]), float(g.loc[m, "tv"]))
        else:
            out[m] = (0, 0.0)
    return out


def has_data(metrics):
    return any(du > 0 or tv > 0 for du, tv in metrics.values())


def collect_rows_for_product(df, product, months):
    """Return list of row dicts (level, outline, name, login, team_size, metrics) for one product."""
    dfp = df[df["application_type"] == product].copy()

    # Build manager metadata restricted to managers with any data for this product,
    # plus their ancestors (we need team_size lookup via full df).
    meta_all = df[["manager_login", "manager_name", "job_level_name", "team_size",
                   "manager_hierarchy"]].drop_duplicates(subset=["manager_login"])
    meta_all["direct_mgr"] = meta_all["manager_hierarchy"].apply(direct_parent)
    meta_all = meta_all.set_index("manager_login")

    # Per-manager metrics for this product
    per_mgr = (
        dfp[dfp["application_type"].notna()]
        .groupby(["manager_login", "month"])
        .agg(du=("distinct_users", "sum"), tv=("total_measure_value", "sum"))
    )

    def get_metrics(login):
        if login not in per_mgr.index.get_level_values(0):
            return {m: (0, 0.0) for m in months}
        g = per_mgr.loc[login]
        out = {}
        for m in months:
            if m in g.index:
                out[m] = (int(g.loc[m, "du"]), float(g.loc[m, "tv"]))
            else:
                out[m] = (0, 0.0)
        return out

    # Lookup helpers
    by_name_lvl = {}
    for login, r in meta_all.iterrows():
        by_name_lvl.setdefault((r["manager_name"], r["job_level_name"]), []).append(login)

    rows = []

    # L11 leaders who have product data
    # Exclude L11s who report through ANOTHER L11 - they will only appear
    # nested beneath their parent L11, not as a separate top-level entry.
    l11_meta = meta_all[meta_all["job_level_name"] == 11]
    l11_names_set = set(l11_meta["manager_name"])
    # A top-level L11 is one whose direct_mgr is NOT another L11
    top_l11 = l11_meta[~l11_meta["direct_mgr"].isin(l11_names_set)]

    l11_candidates = []
    for login, r in top_l11.iterrows():
        m = get_metrics(login)
        if has_data(m):
            l11_candidates.append((r["manager_name"], login, r["team_size"], m))
    l11_candidates.sort(key=lambda x: x[0].lower())

    for name, login, tsize, m in l11_candidates:
        rows.append(dict(level="L11", outline=1, name=name, login=login, team_size=tsize, metrics=m))

        # Direct L11 reports (nested L11 under L11)
        dir_l11 = meta_all[(meta_all["job_level_name"] == 11) & (meta_all["direct_mgr"] == name)]
        for c_login, cr in dir_l11.iterrows():
            cm = get_metrics(c_login)
            if has_data(cm):
                rows.append(dict(level="L11", outline=2, name=cr["manager_name"],
                                 login=c_login,
                                 team_size=cr["team_size"], metrics=cm))
                # Direct L10 reports of that nested L11, then one level under each L10
                dir_l10_nested = meta_all[(meta_all["job_level_name"] == 10) &
                                          (meta_all["direct_mgr"] == cr["manager_name"])]
                for c10_login, c10 in dir_l10_nested.iterrows():
                    c10m = get_metrics(c10_login)
                    if has_data(c10m):
                        rows.append(dict(level="L10", outline=3, name=c10["manager_name"],
                                         login=c10_login,
                                         team_size=c10["team_size"], metrics=c10m))
                        # Direct reports of this L10 (any level, one step deep)
                        dir_any_n = meta_all[meta_all["direct_mgr"] == c10["manager_name"]]
                        dir_any_n = dir_any_n.sort_values(
                            ["job_level_name", "team_size"], ascending=[False, False]
                        )
                        for c_login_n, cn in dir_any_n.iterrows():
                            cnm = get_metrics(c_login_n)
                            if has_data(cnm):
                                rows.append(dict(
                                    level=f"L{int(cn['job_level_name'])}",
                                    outline=4, name=cn["manager_name"],
                                    login=c_login_n,
                                    team_size=cn["team_size"], metrics=cnm,
                                ))

        # Direct L10 reports of the parent L11
        dir_l10 = meta_all[(meta_all["job_level_name"] == 10) & (meta_all["direct_mgr"] == name)]
        for c_login, cr in dir_l10.iterrows():
            cm = get_metrics(c_login)
            if has_data(cm):
                rows.append(dict(level="L10", outline=2, name=cr["manager_name"],
                                 login=c_login,
                                 team_size=cr["team_size"], metrics=cm))
                # Direct reports of the L10 (any level: L10, L8, L7). Capped one level deep.
                dir_any = meta_all[meta_all["direct_mgr"] == cr["manager_name"]]
                # Sort by level desc (higher levels first), then team_size desc
                dir_any = dir_any.sort_values(
                    ["job_level_name", "team_size"], ascending=[False, False]
                )
                for c_login2, c2 in dir_any.iterrows():
                    c2m = get_metrics(c_login2)
                    if has_data(c2m):
                        rows.append(dict(level=f"L{int(c2['job_level_name'])}",
                                         outline=3, name=c2["manager_name"],
                                         login=c_login2,
                                         team_size=c2["team_size"], metrics=c2m))
    return rows


def build_sheet(wb, df, months):
    sheet_name = "Product Rollup by L11"
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)

    # Header
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
    header_fill = PatternFill("solid", fgColor="1F4E78")
    center = Alignment(horizontal="center", vertical="center")
    for col in range(1, len(header2) + 1):
        for row in (1, 2):
            c = ws.cell(row=row, column=col)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center

    ws.sheet_properties.outlinePr.summaryBelow = False
    ws.sheet_properties.outlinePr.summaryRight = False
    # Start collapsed: only outline level 0 (products) visible.
    ws.sheet_format.outlineLevelRow = 0

    # Styling colours per outline level
    level_fill = {
        0: PatternFill("solid", fgColor="305496"),  # product - dark blue
        1: PatternFill("solid", fgColor="8EA9DB"),  # L11
        2: PatternFill("solid", fgColor="D9E1F2"),  # nested L11/L10
        3: PatternFill("solid", fgColor="F2F2F2"),  # L10/L8 (direct under L10)
        4: PatternFill("solid", fgColor="FFFFFF"),  # deepest level
    }
    level_font = {
        0: Font(bold=True, color="FFFFFF"),
        1: Font(bold=True),
        2: Font(bold=False),
        3: Font(bold=False, italic=True),
        4: Font(bold=False, italic=True, color="555555"),
    }

    products = sorted(df["application_type"].dropna().unique(), key=str.lower)
    current_row = 3

    for product in products:
        print(f"  Building rows for product: {product}")
        prod_rows = collect_rows_for_product(df, product, months)
        if not prod_rows:
            print(f"    (no data - skipping)")
            continue

        # Product header row (outline 0)
        row_vals = [product, "Product", None, None, None] + [None, None] * len(months)
        ws.append(row_vals)
        for col in range(1, len(row_vals) + 1):
            c = ws.cell(row=current_row, column=col)
            c.font = level_font[0]
            c.fill = level_fill[0]
        current_row += 1

        # Child rows
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

    # Freeze panes and widths
    ws.freeze_panes = "F3"
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 8
    ws.column_dimensions["C"].width = 11
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 12
    for i in range(len(months)):
        ws.column_dimensions[get_column_letter(6 + i * 2)].width = 14
        ws.column_dimensions[get_column_letter(7 + i * 2)].width = 12


def validate(df, months):
    """Check EVERY data row against direct source aggregation, using the Login column
    to disambiguate duplicate manager names."""
    wb = load_workbook(SRC)
    ws = wb["Product Rollup by L11"]
    month_cols = {}
    for i, m in enumerate(months):
        month_cols[m] = (6 + i * 2, 7 + i * 2)  # Login is now col 5

    mismatches = 0
    checks = 0
    product_ctx = None

    for row in range(3, ws.max_row + 1):
        level_val = ws.cell(row=row, column=2).value
        name_raw = ws.cell(row=row, column=1).value or ""
        login = ws.cell(row=row, column=5).value

        if level_val == "Product":
            product_ctx = name_raw.strip()
            continue
        if not login:
            continue

        sub = df[(df["manager_login"] == login) & (df["application_type"] == product_ctx)]
        g = sub.groupby("month").agg(du=("distinct_users", "sum"), tv=("total_measure_value", "sum"))
        for m, (cdu, ctv) in month_cols.items():
            exp_du = int(g.loc[m, "du"]) if m in g.index else 0
            exp_tv = float(g.loc[m, "tv"]) if m in g.index else 0.0
            got_du = ws.cell(row=row, column=cdu).value or 0
            got_tv = ws.cell(row=row, column=ctv).value or 0
            checks += 2
            if int(got_du) != exp_du:
                mismatches += 1
                if mismatches <= 10:
                    print(f"  MISMATCH DU row={row} [{product_ctx} | {name_raw.strip()} ({login}) | {m}]: got {got_du} vs expected {exp_du}")
            if abs(float(got_tv) - exp_tv) > 0.01:
                mismatches += 1
                if mismatches <= 10:
                    print(f"  MISMATCH TV row={row} [{product_ctx} | {name_raw.strip()} ({login}) | {m}]: got {got_tv} vs expected {exp_tv}")

    print(f"\nValidation: {checks} cells checked across all rows, {mismatches} mismatches")


def main():
    df = load_source()
    months = sorted([m for m in df["month"].dropna().unique()], reverse=True)
    print(f"Months: {months}")

    wb = load_workbook(SRC)
    build_sheet(wb, df, months)
    wb.save(SRC)
    print(f"\nSaved to {SRC}")

    validate(df, months)


if __name__ == "__main__":
    main()
