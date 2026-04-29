"""Build the 'Tobias - Product Breakdown' flat sheet.

Layout:
  Row 1: Title + metric selector dropdown
  Row 2: blank
  Row 3: Merged month labels (one label spanning 3 columns per month)
  Row 4: Per-month sub-headers ('Distinct Users' | 'Total Views' | '[selected metric]')
  Row 5+: Data rows, one per (product, leader). Products sorted alphabetically.

Per month block: 3 columns.
  Col 1 (DU): integer value
  Col 2 (TV): numeric value
  Col 3 (selected metric): Excel formula that switches based on the selector cell.

Selector options (value in the dropdown cell):
  - Total Views per User (TV/DU)   [default]
  - MoM % delta Distinct Users
  - MoM % delta Total Views
  - MoM % delta (Total Views per User)
"""
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule

BASE = "/Users/propatil/Desktop/Other Projects/TPM_Related/Products Usage Metrics/Excel Analysis"
OP = os.path.join(BASE, "usage metrics op_excellence_20260420_v1.xlsx")
QS = os.path.join(BASE, "QuickSight_UsageMetrics_ExclFintech_20260420_v1.xlsx")
TBU = os.path.join(BASE, "Tableau UniquerUsers_ExclFinTech_20260420_v1.xlsx")
TBV = os.path.join(BASE, "Tableau TotalViews_ExclFinTech_20260420_v1.xlsx")
HIER = os.path.join(BASE, "das_finops_op_excellmployee_hierarchy_all.xlsx")

TOBIAS = "tobias"
SHEET_NAME = "Tobias - Product Breakdown"

METRIC_OPTIONS = [
    "Total Views per User (TV/DU)",
    "MoM % Delta Distinct Users",
    "MoM % Delta Total Views",
    "MoM % Delta (Total Views per User)",
]
DEFAULT_METRIC = METRIC_OPTIONS[0]


# Reuse the data loaders from the integrated rollup build.
# We import the module by adjusting sys.path so the script is self-contained.
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_integrated_rollup_v1 import (
    load_hierarchy, load_op_excellence, build_dashboard_avenue,
    load_tableau_filter, load_manager_meta, TBU as _TBU_PATH, TBV as _TBV_PATH,
    AVENUE_OP, AVENUE_DASH,
)


def load_combined_agg():
    """Return combined (product, leader, month) data summed across avenues.
    Matches the 'Product Rollup by L11' numbers for Tobias.
    """
    chain_map = load_hierarchy()
    op = load_op_excellence()
    tbu_keep = load_tableau_filter(_TBU_PATH, "Filtered Dashboards")
    tbv_keep = load_tableau_filter(_TBV_PATH, "Dasboards")
    dash, _qs_events, _tbu_long, _tbv_long = build_dashboard_avenue(
        chain_map, None, tbu_keep, tbv_keep
    )
    both = pd.concat([op, dash], ignore_index=True)
    # Sum across avenues per (manager_login, product, month)
    combined = both.groupby(["manager_login", "product", "month"]).agg(
        distinct_users=("distinct_users", "sum"),
        total_views=("total_views", "sum"),
    ).reset_index()
    return combined


def get_tobias_directs(meta):
    """Return list of (login, name, level, team_size) for direct reports of Tobias."""
    tobias_row = meta[meta.index == TOBIAS]
    if tobias_row.empty:
        raise RuntimeError("Tobias not found in manager meta")
    tobias_name = tobias_row["manager_name"].iloc[0]
    directs = meta[meta["direct_mgr"] == tobias_name].copy()
    directs = directs.sort_values(["job_level_name", "team_size"], ascending=[False, False])
    out = []
    for login, row in directs.iterrows():
        out.append((login, row["manager_name"], int(row["job_level_name"]), int(row["team_size"])))
    return tobias_name, out


def short_month(m):
    """Convert '2026-04' to 'Apr-26'."""
    ts = pd.to_datetime(m + "-01")
    return ts.strftime("%b-%y")


def build_sheet(wb, combined, meta, months):
    if SHEET_NAME in wb.sheetnames:
        del wb[SHEET_NAME]
    ws = wb.create_sheet(SHEET_NAME)

    # Colour palette (muted)
    title_fill = PatternFill("solid", fgColor="4F6D7A")
    header_fill = PatternFill("solid", fgColor="4F6D7A")
    parent_fill = PatternFill("solid", fgColor="D8E2DC")
    child_fill = PatternFill("solid", fgColor="F8F5F2")
    selector_fill = PatternFill("solid", fgColor="FFF3B0")

    white_bold = Font(bold=True, color="FFFFFF")
    dark_bold = Font(bold=True, color="2F4858")
    center = Alignment(horizontal="center", vertical="center")
    thin = Side(border_style="thin", color="B0B0B0")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # Row 1: title + metric selector
    ws.cell(row=1, column=1, value="Tobias Straub - Product Breakdown").font = Font(
        bold=True, size=14, color="2F4858"
    )
    ws.cell(row=1, column=6, value="Extra metric:").font = Font(bold=True, color="2F4858")
    ws.cell(row=1, column=6).alignment = Alignment(horizontal="right", vertical="center")
    selector_cell = ws.cell(row=1, column=7, value=DEFAULT_METRIC)
    selector_cell.font = Font(bold=True, color="2F4858")
    selector_cell.fill = selector_fill
    selector_cell.border = border
    # Data validation dropdown
    dv = DataValidation(
        type="list",
        formula1='"' + ",".join(METRIC_OPTIONS) + '"',
        allow_blank=False,
    )
    dv.add(selector_cell.coordinate)
    ws.add_data_validation(dv)
    ws.merge_cells(start_row=1, end_row=1, start_column=7, end_column=11)
    ws.row_dimensions[1].height = 22

    # Row 3: month group labels (merged across 3 columns each)
    # Row 4: sub-headers
    n_months = len(months)
    static_headers = ["Product", "Leader", "Level", "Team Size", "Entitled Users"]
    n_static = len(static_headers)

    for i, h in enumerate(static_headers, start=1):
        ws.cell(row=3, column=i, value=h).font = white_bold
        ws.cell(row=3, column=i).fill = header_fill
        ws.cell(row=3, column=i).alignment = center
        ws.cell(row=3, column=i).border = border
        ws.merge_cells(start_row=3, end_row=4, start_column=i, end_column=i)

    for j, m in enumerate(months):
        start_col = n_static + 1 + j * 3
        end_col = start_col + 2
        lbl = short_month(m)
        ws.cell(row=3, column=start_col, value=lbl).font = white_bold
        ws.cell(row=3, column=start_col).fill = header_fill
        ws.cell(row=3, column=start_col).alignment = center
        ws.cell(row=3, column=start_col).border = border
        ws.merge_cells(start_row=3, end_row=3, start_column=start_col, end_column=end_col)
        # sub-headers on row 4
        subs = ["Distinct Users", "Total Views", "[Metric]"]
        for k, sub in enumerate(subs):
            c = ws.cell(row=4, column=start_col + k, value=sub)
            c.font = white_bold
            c.fill = header_fill
            c.alignment = center
            c.border = border

    # Determine products: any where Tobias OR any direct had activity in any month
    tobias_name, directs = get_tobias_directs(meta)
    direct_logins = [d[0] for d in directs]
    all_logins = [TOBIAS] + direct_logins

    products_touched = sorted(
        combined[combined["manager_login"].isin(all_logins)]["product"].dropna().unique(),
        key=str.lower,
    )

    # For each product, emit Tobias row + directs rows (only those with activity in that product)
    current_row = 5
    for product in products_touched:
        # Tobias data for this product
        tob_sub = combined[(combined["manager_login"] == TOBIAS) & (combined["product"] == product)]
        if tob_sub.empty:
            # Tobias has no data, but a direct might - include with zeros for Tobias to signal gap
            continue

        # Active directs for this product
        active_directs = []
        for login, name, level, tsize in directs:
            sub = combined[(combined["manager_login"] == login) & (combined["product"] == product)]
            if not sub.empty and (sub["distinct_users"].sum() > 0 or sub["total_views"].sum() > 0):
                active_directs.append((login, name, level, tsize))

        # Parent row (Tobias)
        _emit_row(ws, current_row, product, tobias_name, "L10",
                  int(meta.loc[TOBIAS, "team_size"]),
                  _metrics_map(tob_sub, months), months, n_static,
                  selector_cell.coordinate, parent_fill, dark_bold, border)
        current_row += 1

        # Direct rows (blank product label for cleaner look, still keep Product in col A for filterability)
        for login, name, level, tsize in active_directs:
            sub = combined[(combined["manager_login"] == login) & (combined["product"] == product)]
            _emit_row(ws, current_row, product, name, f"L{level}", tsize,
                      _metrics_map(sub, months), months, n_static,
                      selector_cell.coordinate, child_fill, Font(), border)
            current_row += 1

    # Column widths
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 7
    ws.column_dimensions["D"].width = 11
    ws.column_dimensions["E"].width = 14
    for j in range(n_months):
        col = n_static + 1 + j * 3
        ws.column_dimensions[get_column_letter(col)].width = 13
        ws.column_dimensions[get_column_letter(col + 1)].width = 13
        ws.column_dimensions[get_column_letter(col + 2)].width = 15

    ws.freeze_panes = "F5"

    # Sub-header "[Metric]" should reflect the selector text so the user always
    # sees which metric the 3rd column is showing. Formula references selector.
    for j in range(n_months):
        start_col = n_static + 1 + j * 3
        cell = ws.cell(row=4, column=start_col + 2)
        cell.value = f"={selector_cell.coordinate}"

    # Conditional formatting for MoM metric cells (green positive, red negative)
    last_row = current_row - 1
    if last_row >= 5:
        metric_col_letters = [
            get_column_letter(n_static + 1 + j * 3 + 2) for j in range(n_months)
        ]
        for col_letter in metric_col_letters:
            rng = f"{col_letter}5:{col_letter}{last_row}"
            # green for positive, red for negative (use CellIs rules)
            ws.conditional_formatting.add(
                rng,
                CellIsRule(operator="greaterThan", formula=["0"],
                           fill=PatternFill("solid", fgColor="C6EFCE")),
            )
            ws.conditional_formatting.add(
                rng,
                CellIsRule(operator="lessThan", formula=["0"],
                           fill=PatternFill("solid", fgColor="FFC7CE")),
            )


def _metrics_map(sub_df, months):
    out = {}
    for m in months:
        r = sub_df[sub_df["month"] == m]
        if r.empty:
            out[m] = (0, 0.0)
        else:
            out[m] = (int(r["distinct_users"].iloc[0]), float(r["total_views"].iloc[0]))
    return out


def _emit_row(ws, row, product, leader, level, tsize, metrics, months, n_static,
              selector_coord, fill, font, border):
    ws.cell(row=row, column=1, value=product)
    ws.cell(row=row, column=2, value=leader)
    ws.cell(row=row, column=3, value=level)
    ws.cell(row=row, column=4, value=tsize)
    ws.cell(row=row, column=5, value=None)  # entitled users blank
    for j, m in enumerate(months):
        du, tv = metrics[m]
        c_du = ws.cell(row=row, column=n_static + 1 + j * 3, value=int(du))
        c_tv = ws.cell(row=row, column=n_static + 1 + j * 3 + 1, value=round(tv, 2))
        c_metric = ws.cell(row=row, column=n_static + 1 + j * 3 + 2)
        # Build the conditional formula for the selected metric
        du_cell = c_du.coordinate
        tv_cell = c_tv.coordinate
        if j + 1 < len(months):
            # Previous month (to the right, since descending)
            prev_du = ws.cell(row=row, column=n_static + 1 + (j + 1) * 3).coordinate
            prev_tv = ws.cell(row=row, column=n_static + 1 + (j + 1) * 3 + 1).coordinate
        else:
            prev_du = None
            prev_tv = None

        # IFS chain: which metric based on selector_coord
        tv_over_du = f"IFERROR({tv_cell}/{du_cell},\"\")"
        if prev_du is not None:
            mom_du = f"IFERROR(({du_cell}-{prev_du})/{prev_du},\"\")"
            mom_tv = f"IFERROR(({tv_cell}-{prev_tv})/{prev_tv},\"\")"
            mom_tv_du = (
                f"IFERROR((({tv_cell}/{du_cell})-({prev_tv}/{prev_du}))/({prev_tv}/{prev_du}),\"\")"
            )
        else:
            mom_du = '""'
            mom_tv = '""'
            mom_tv_du = '""'

        formula = (
            f'=IF({selector_coord}="{METRIC_OPTIONS[0]}",{tv_over_du},'
            f'IF({selector_coord}="{METRIC_OPTIONS[1]}",{mom_du},'
            f'IF({selector_coord}="{METRIC_OPTIONS[2]}",{mom_tv},'
            f'IF({selector_coord}="{METRIC_OPTIONS[3]}",{mom_tv_du},""))))'
        )
        c_metric.value = formula

    # Style / number format
    for col in range(1, n_static + 1 + len(months) * 3 + 1):
        c = ws.cell(row=row, column=col)
        c.font = font
        c.fill = fill
        c.border = border
        if col == 4:  # team size
            c.alignment = Alignment(horizontal="right")
        elif col == 3 or col == 5:
            c.alignment = Alignment(horizontal="center")
        elif col <= n_static:
            c.alignment = Alignment(horizontal="left")

    # Number formats for month columns
    for j in range(len(months)):
        du_col = n_static + 1 + j * 3
        tv_col = du_col + 1
        metric_col = du_col + 2
        ws.cell(row=row, column=du_col).number_format = "#,##0"
        ws.cell(row=row, column=tv_col).number_format = "#,##0"
        # Metric column format depends on selector but Excel can't conditionally
        # change number_format based on cell value. We use a format that works
        # reasonably for all: a positive ratio (TV/DU) and a percentage.
        # Compromise: use percent format with 1 decimal. TV/DU values (e.g., 3.5)
        # would show as 350.0% - not ideal. Use a custom format that handles both
        # by detecting magnitude.
        # Better approach: use a number format that shows 2 decimals with no %
        # sign; user toggles selector and mentally reads context.
        # For MoM metrics the values are fractions like 0.123 = 12.3%.
        # Simplest: show as percentage with 1 decimal. For TV/DU this shows
        # e.g., 3.75 as 375.0% which is confusing.
        # Use conditional format via number_format = "0.00;-0.00" and put a
        # note next to the selector explaining the format.
        ws.cell(row=row, column=metric_col).number_format = "0.00;-0.00"
        ws.cell(row=row, column=metric_col).alignment = Alignment(horizontal="right")


def main():
    print("Loading combined aggregate ...")
    combined = load_combined_agg()
    meta = load_manager_meta()
    months = sorted(combined["month"].dropna().unique(), reverse=True)
    print(f"Months: {months}")

    wb = load_workbook(OP)
    build_sheet(wb, combined, meta, months)
    wb.save(OP)
    print(f"Saved sheet '{SHEET_NAME}' to {os.path.basename(OP)}")

    # Verify Tobias numbers match the main rollup sheet
    print("\nVerifying Tobias numbers match 'Product Rollup by L11' ...")
    wb2 = load_workbook(OP)
    main_ws = wb2["Product Rollup by L11"]
    new_ws = wb2[SHEET_NAME]

    # Find Tobias rows in main sheet (all occurrences)
    main_tobias = {}  # (product) -> dict[month_yyyy_mm] -> (du, tv)
    current_product = None
    # products may have avenue rows; we need the sum-across-avenues per product
    month_cols_main = {}
    for col in range(6, main_ws.max_column + 1, 2):
        lbl = main_ws.cell(row=1, column=col).value
        if isinstance(lbl, str) and "-" in lbl and len(lbl) == 7:
            month_cols_main[lbl] = (col, col + 1)
    for row in range(3, main_ws.max_row + 1):
        level = main_ws.cell(row=row, column=2).value
        login = main_ws.cell(row=row, column=5).value
        name = (main_ws.cell(row=row, column=1).value or "").strip()
        if level == "Product":
            current_product = name
            continue
        if login == TOBIAS:
            # Sum across avenue occurrences
            d = main_tobias.setdefault(current_product, {})
            for m, (cdu, ctv) in month_cols_main.items():
                du = main_ws.cell(row=row, column=cdu).value or 0
                tv = main_ws.cell(row=row, column=ctv).value or 0
                prev = d.get(m, (0, 0))
                d[m] = (prev[0] + int(du), prev[1] + float(tv))

    # Find Tobias rows in new sheet
    n_static = 5
    month_cols_new = {}
    for j, m in enumerate(months):
        # Use full 'YYYY-MM' as key to match month_cols_main
        col = n_static + 1 + j * 3
        month_cols_new[m] = (col, col + 1)

    mismatches = 0
    checks = 0
    for row in range(5, new_ws.max_row + 1):
        product = new_ws.cell(row=row, column=1).value
        leader = new_ws.cell(row=row, column=2).value
        if leader != "Tobias Straub":
            continue
        for m, (du_col, tv_col) in month_cols_new.items():
            new_du = new_ws.cell(row=row, column=du_col).value or 0
            new_tv = new_ws.cell(row=row, column=tv_col).value or 0
            expected = main_tobias.get(product, {}).get(m, (0, 0))
            checks += 2
            if int(new_du) != expected[0]:
                mismatches += 1
                print(f"  MISMATCH DU [{product}|{m}]: new={new_du} main={expected[0]}")
            if abs(float(new_tv) - expected[1]) > 0.01:
                mismatches += 1
                print(f"  MISMATCH TV [{product}|{m}]: new={new_tv} main={expected[1]}")
    print(f"  Tobias rows: {checks} cells checked, {mismatches} mismatches")


if __name__ == "__main__":
    main()
