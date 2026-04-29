"""
Build an L11 rollup view from usage metrics op_excellence_20260415.xlsx.

Layout
------
For each L11 leader (sorted descending by team_size), build a parent row.
Below it (collapsible) add one row per DIRECT report that is an L11 or L10 under
that L11. Metrics are each manager's OWN roll-up (source of truth), which by
construction already aggregates the entire subordinate tree. No summing of
child rows is done. That avoids double-counting an L11-under-L11 or an L10
whose rollup is already contained in the parent L11's row.

Columns
-------
A: Leader / sub-leader name (indented by level for readability)
B: Level (L11 / L10)
C: team_size
D: entitled_users (empty - user fills in)
E..: One pair of columns per month in DESCENDING month order:
        <YYYY-MM> Distinct Users | <YYYY-MM> Total Views

The source rows with NaN application are "no-usage" placeholders (distinct_users
= 0). We drop those when aggregating usage. When a manager has no usage rows
at all they still appear with zeros.

Validation
----------
After writing, compare selected L11 monthly totals against a direct aggregate
of that same L11's rows read from the source sheet.
"""
import os
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = "/Users/propatil/Desktop/Other Projects/TPM_Related/Products Usage Metrics/Excel Analysis"
SRC = os.path.join(BASE, "usage metrics op_excellence_20260415.xlsx")
OUT = os.path.join(BASE, "usage metrics op_excellence_20260415.xlsx")  # add sheets in place


def month_of(d):
    ts = pd.to_datetime(d, errors="coerce")
    if pd.isna(ts):
        return None
    return ts.strftime("%Y-%m")


def load_source():
    df = pd.read_excel(SRC, sheet_name="Result 1")
    df["month"] = df["log_week"].apply(month_of)
    return df


def build_manager_frames(df):
    """Return (l11_list, l10_list) of dicts with name, login, team_size, direct_mgr_name."""
    meta_cols = ["manager_login", "manager_name", "job_level_name", "team_size", "manager_hierarchy"]
    mgrs = df[meta_cols].drop_duplicates(subset=["manager_login"])
    mgrs["direct_mgr"] = mgrs["manager_hierarchy"].apply(
        lambda h: h.split(":")[1] if isinstance(h, str) and len(h.split(":")) > 1 else None
    )
    l11 = mgrs[mgrs["job_level_name"] == 11].copy()
    l10 = mgrs[mgrs["job_level_name"] == 10].copy()
    return l11, l10


def monthly_metrics(df, manager_login):
    """Return dict: month -> (distinct_users, total_views) for a single manager,
    summed across products. distinct_users across products is summed (this
    matches how the source file presents the data: per-row distinct_users is
    per (manager, week, product)). Note: summing distinct_users across products
    for the same month can overcount a user who uses two products. The source
    data does not allow a true cross-product distinct count, so this matches
    the file's native granularity.
    """
    sub = df[df["manager_login"] == manager_login]
    sub = sub[sub["application"].notna()]
    if sub.empty:
        return {}
    g = sub.groupby("month").agg(
        distinct_users=("distinct_users", "sum"),
        total_views=("total_measure_value", "sum"),
    )
    return g.to_dict("index")


def monthly_metrics_by_product(df, manager_login):
    """Return dict: (month, product) -> (distinct_users, total_views)."""
    sub = df[df["manager_login"] == manager_login]
    sub = sub[sub["application"].notna()]
    if sub.empty:
        return {}
    g = sub.groupby(["month", "application_type"]).agg(
        distinct_users=("distinct_users", "sum"),
        total_views=("total_measure_value", "sum"),
    )
    return g.to_dict("index")


def build_rollup(df, by_product=False):
    l11, l10 = build_manager_frames(df)
    l11_names = set(l11["manager_name"])

    # Map name -> login (names may have duplicates; fall back to the first login)
    name_to_login = {}
    for _, r in pd.concat([l11, l10]).iterrows():
        name_to_login.setdefault(r["manager_name"], r["manager_login"])

    # Order L11s by team_size desc
    l11_sorted = l11.sort_values("team_size", ascending=False)

    rows = []  # list of dicts (for later writing)
    for _, l11_row in l11_sorted.iterrows():
        parent_login = l11_row["manager_login"]
        parent_name = l11_row["manager_name"]
        parent_size = l11_row["team_size"]
        parent_metrics = monthly_metrics(df, parent_login)
        rows.append(
            {
                "level": "L11",
                "outline": 0,
                "name": parent_name,
                "login": parent_login,
                "team_size": parent_size,
                "metrics": parent_metrics,
            }
        )

        # Direct L11 reports
        child_l11 = l11[l11["direct_mgr"] == parent_name].sort_values("team_size", ascending=False)
        for _, cr in child_l11.iterrows():
            rows.append(
                {
                    "level": "L11",
                    "outline": 1,
                    "name": cr["manager_name"],
                    "login": cr["manager_login"],
                    "team_size": cr["team_size"],
                    "metrics": monthly_metrics(df, cr["manager_login"]),
                }
            )
        # Direct L10 reports
        child_l10 = l10[l10["direct_mgr"] == parent_name].sort_values("team_size", ascending=False)
        for _, cr in child_l10.iterrows():
            rows.append(
                {
                    "level": "L10",
                    "outline": 1,
                    "name": cr["manager_name"],
                    "login": cr["manager_login"],
                    "team_size": cr["team_size"],
                    "metrics": monthly_metrics(df, cr["manager_login"]),
                }
            )
    return rows


def write_sheet(wb, sheet_name, rows, months_desc):
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)

    # Header row 1 (merged month labels) + row 2 (sub-headers)
    header1 = ["Leader", "Level", "Team Size", "Entitled Users"]
    for m in months_desc:
        header1.extend([m, ""])  # will merge later
    header2 = ["", "", "", ""]
    for _ in months_desc:
        header2.extend(["Distinct Users", "Total Views"])

    ws.append(header1)
    ws.append(header2)

    # Merge month label cells in row 1
    for i, _m in enumerate(months_desc):
        start_col = 5 + i * 2
        end_col = start_col + 1
        ws.merge_cells(
            start_row=1, end_row=1, start_column=start_col, end_column=end_col
        )

    # Style
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="1F4E78")
    center = Alignment(horizontal="center", vertical="center")
    for col in range(1, len(header2) + 1):
        c1 = ws.cell(row=1, column=col)
        c2 = ws.cell(row=2, column=col)
        c1.font = header_font
        c1.fill = header_fill
        c1.alignment = center
        c2.font = header_font
        c2.fill = header_fill
        c2.alignment = center

    # Data rows
    current_excel_row = 3
    for r in rows:
        indent = "    " * r["outline"]
        row_vals = [
            indent + r["name"],
            r["level"],
            r["team_size"],
            None,  # entitled users blank
        ]
        metrics = r["metrics"]
        for m in months_desc:
            mdict = metrics.get(m)
            if mdict:
                row_vals.extend([int(mdict["distinct_users"]), mdict["total_views"]])
            else:
                row_vals.extend([0, 0])
        ws.append(row_vals)
        if r["outline"] > 0:
            ws.row_dimensions[current_excel_row].outline_level = r["outline"]
            ws.row_dimensions[current_excel_row].hidden = True  # collapsed by default
        # Bold the parent L11 rows
        if r["outline"] == 0:
            for col in range(1, len(row_vals) + 1):
                ws.cell(row=current_excel_row, column=col).font = Font(bold=True)
        current_excel_row += 1

    # Set outline summary below/right (Excel default)
    ws.sheet_properties.outlinePr.summaryBelow = False
    ws.sheet_properties.outlinePr.summaryRight = False

    # Freeze panes and column widths
    ws.freeze_panes = "E3"
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 7
    ws.column_dimensions["C"].width = 11
    ws.column_dimensions["D"].width = 14
    for i in range(len(months_desc)):
        col1 = get_column_letter(5 + i * 2)
        col2 = get_column_letter(6 + i * 2)
        ws.column_dimensions[col1].width = 14
        ws.column_dimensions[col2].width = 12


def main():
    df = load_source()
    print(f"Loaded {len(df)} rows")
    months = sorted([m for m in df["month"].dropna().unique()], reverse=True)
    print(f"Months: {months}")

    rollup = build_rollup(df)

    # Open source workbook and add the sheet
    wb = load_workbook(SRC)
    write_sheet(wb, "L11 Rollup by Month", rollup, months)
    wb.save(OUT)
    print(f"Wrote sheet 'L11 Rollup by Month' to {OUT}")

    # ---- Validation ----
    print("\n" + "=" * 70)
    print("VALIDATION: spot-check parent totals against direct source aggregation")
    print("=" * 70)
    sample_logins = ["dherring", "uditm", "garman", "olsavsky"]
    for lg in sample_logins:
        sub = df[(df["manager_login"] == lg) & df["application"].notna()]
        g = (
            sub.groupby("month")
            .agg(
                distinct_users=("distinct_users", "sum"),
                total_views=("total_measure_value", "sum"),
            )
            .sort_index(ascending=False)
        )
        print(f"\n[{lg}] from source (all products, per month):")
        print(g.to_string())

    # Also: assert that for each parent L11 row, the values we wrote equal the direct source aggregate
    wb2 = load_workbook(OUT)
    ws = wb2["L11 Rollup by Month"]
    month_cols = {}
    for i, m in enumerate(months):
        month_cols[m] = (5 + i * 2, 6 + i * 2)

    mismatches = 0
    checks = 0
    for row in range(3, ws.max_row + 1):
        level = ws.cell(row=row, column=2).value
        name_cell = ws.cell(row=row, column=1).value or ""
        outline = ws.row_dimensions[row].outline_level or 0
        if level != "L11" or outline != 0:
            continue
        name = name_cell.strip()
        # resolve login
        meta = df[(df["manager_name"] == name) & (df["job_level_name"] == 11)]
        if meta.empty:
            continue
        login = meta["manager_login"].iloc[0]
        sub = df[(df["manager_login"] == login) & df["application"].notna()]
        g = sub.groupby("month").agg(
            du=("distinct_users", "sum"), tv=("total_measure_value", "sum")
        )
        for m, (col_du, col_tv) in month_cols.items():
            expected_du = int(g.loc[m, "du"]) if m in g.index else 0
            expected_tv = float(g.loc[m, "tv"]) if m in g.index else 0.0
            got_du = ws.cell(row=row, column=col_du).value or 0
            got_tv = ws.cell(row=row, column=col_tv).value or 0
            checks += 2
            if int(got_du) != expected_du:
                print(f"MISMATCH DU [{name} {m}]: got {got_du} expected {expected_du}")
                mismatches += 1
            if abs(float(got_tv) - expected_tv) > 1e-6:
                print(f"MISMATCH TV [{name} {m}]: got {got_tv} expected {expected_tv}")
                mismatches += 1

    print(f"\nValidation: {checks} cells checked, {mismatches} mismatches")


if __name__ == "__main__":
    main()
