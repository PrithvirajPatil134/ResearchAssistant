# Product Usage Metrics — Monthly Refresh Process

This document captures the end-to-end process for refreshing the monthly product usage metrics rollup. When sources are refreshed each month, point the model at this doc + the new files and the script will regenerate the `Product Rollup by L11` sheet.

## Location

Source files live in:
`/Users/propatil/Desktop/Other Projects/TPM_Related/Products Usage Metrics/Excel Analysis/`

Build script: `scripts/build_integrated_rollup_v1.py` (Python 3.9+, pandas 2+, openpyxl 3+)

## Input files expected

Four source workbooks plus one lookup file:

1. **Op Excellence rollup**
   - Filename pattern: `usage metrics op_excellence_YYYYMMDD_v*.xlsx`
   - Sheet: `Result 1`
   - Key columns: `manager_login`, `manager_name`, `job_level_name`, `team_size`, `manager_hierarchy`, `log_month` (first-of-month date), `application_type`, `application`, `distinct_users`, `total_measure_value`
   - Products expected (case-sensitive): Akara, Ask Rino, Axis, Bluey, Dice-RL, Gandalf, Inventory Reporting, Other DSDI Tools, PDP Financials, Yeti BOM, xVT
     - If the SQL returns "Other FDA Tools" instead of "Inventory Reporting", either rename in source or add a mapping in `load_op_excellence()`.

2. **QuickSight usage metrics**
   - Filename pattern: `QuickSight_UsageMetrics_ExclFintech_YYYYMMDD_v*.xlsx`
   - Sheet: `sheet1`
   - Structure: Tableau-style crosstab with two sections (Axis Monthly + Cerberus). For each section:
     - One "dashboard header" row carrying subtotals
     - Immediately followed by a "NaN user" row carrying unattributed event counts
     - Then one row per user login with per-month `login_id` (1/blank presence flag) and `eventname` (event count)
   - Row ranges used by the script (0-indexed on raw read):
     - Axis Monthly header: row 7
     - Axis Monthly user rows: 9–101 inclusive
     - Cerberus header: row 102
     - Cerberus user rows: 104–258 inclusive
   - **If the row ranges shift** (e.g., more users in either section next month) update the constants `QS_AXIS_ROWS` and `QS_CERBERUS_ROWS` in the script. Row 4 is month labels, row 5 is `login_id`/`eventname` sub-headers.
   - Calculation rule (per Sheet2 note from the original file):
     - `total_views` = count of `eventname` per month
     - `unique_users` = distinct count of `login_id` per month

3. **Tableau Unique Users**
   - Filename pattern: `Tableau UniquerUsers_ExclFinTech_YYYYMMDD_v*.xlsx`
   - Sheet: `Sheet 1` (crosstab, header row 2)
   - Column D (header row names it `Column 4`): viewer login
   - Column B (`Column2`): dashboard name
   - Monthly columns: labels like `4/1/2026 12:00:00 AM`, values are 1 (active that month) or blank
   - Filter sheet: `Filtered Dashboards` listing the 13 dashboards to include

4. **Tableau Total Views**
   - Filename pattern: `Tableau TotalViews_ExclFinTech_YYYYMMDD_v*.xlsx`
   - Sheet: `Sheet 1` (crosstab, header row 2)
   - Columns: `Project`, `Dashboard`, `Owner`, `Viewer` (Column D), `Department`, `Total`, then monthly columns
   - Values: monthly view counts
   - Filter sheet: `Dasboards` (note typo, missing `h`)

5. **Employee hierarchy lookup**
   - Filename: `das_finops_op_excellmployee_hierarchy_all.xlsx`
   - Sheet: `Result 1`
   - Columns: `login_name`, `employee_name`, `manager_login_hierarchy_concat` (colon-separated), `manager_name_hierarchy_concat`, `manager_job_level_hierarchy_concat`
   - Used to map any QuickSight/Tableau login back to its full manager chain.

## Filter dashboards (13)

Maintained in the `Filtered Dashboards` / `Dasboards` tabs of the Tableau files. Current list:

- Inventory Reporting
- DEV Model Input Inspector
- Quest - QxG Retro Analysis - MBR View
- Quest - Planning Cycle Audit Review
- Golem - DEV Waterfall Bridging Dashboard
- Sasquatch LTV
- Yeti BOM
- Yeti BOM Volume and Tier Reports v3
- Yeti BOM Snapshot Data
- Yeti BOM programs with negative incremental volume
- RL-Repair Cost Report_V2
- IBVLF_Physical DEV_Dashboard
- Yeti BOM Live Data

## Product consolidation rules

Multiple source dashboards roll up into unified products:

| Unified product | Sources |
|---|---|
| Axis | op_excellence `Axis` + QuickSight `Axis Monthly` |
| Inventory Reporting | op_excellence `Inventory Reporting` + Tableau `Inventory Reporting` |
| Yeti BOM | op_excellence `Yeti BOM` + any Tableau dashboard whose name contains `Yeti BOM` |
| Cerberus | QuickSight `Cerberus` |
| Each remaining Tableau dashboard in the filter | Standalone product under its own name |

## Merge rule

**Option C (additive):** for each (product, avenue, leader, month), sum metrics across sources. If the same user accesses a product via two avenues, they are counted in both avenues. The rationale is to answer "how many users are using the product via each access path."

## Avenue layer

Products that exist in more than one source show an Avenue layer:

- `Op Excellence` — data from the op_excellence rollup
- `Dashboard` — data from QuickSight or Tableau event-level sources

Single-source products skip the avenue row (product row is that sole avenue).

## Output sheet

Sheet name: `Product Rollup by L11` written to the Op Excellence workbook (e.g., `usage metrics op_excellence_YYYYMMDD_v*.xlsx`).

Hierarchy (Excel outline levels):

- 0 Product
- 1 Avenue (only when >1 avenue)
- 2 L11 leader
- 3 Direct L11 or L10 report of leader
- 4 Direct reports of L10 (L10, L8, L7, etc., one level deep)

Rules:

- Only top-level L11s appear at the leader level (L11s that report through another L11 appear only as nested children of their parent L11).
- Each leader row uses that manager's own rollup for the product+avenue (no child-sum at parent). This avoids double-counting when an L11 reports through another L11.
- Product row = sum of avenue rows. Avenue row = sum of top-level L11 rows within that avenue.
- Leaders without any activity for a product are not shown.
- All non-product rows are collapsed by default (use the `+` in the Excel outline gutter to expand).

Column layout:

| Col | Header |
|---|---|
| A | Leader / Product |
| B | Level (Product / Avenue / L11 / L10 / L8 / L7) |
| C | Team Size |
| D | Entitled Users (left blank for manual fill-in) |
| E | Login (manager_login or blank for Product/Avenue rows) |
| F+ | Month pairs `Distinct Users` \| `Total Views`, descending order |

## Consolidated users sheet

A second sheet named `consolidated users` is written to the QuickSight workbook listing every login found across QuickSight, Tableau Unique Users, and Tableau Total Views, with flags indicating which sources each login appears in and whether the login resolves in the hierarchy file.

Columns: `login`, `employee_name`, `in_hierarchy`, `in_quicksight`, `in_tableau_unique_users`, `in_tableau_total_views`.

Use this to identify logins that cannot be credited to a manager (in_hierarchy = No).

## Validation built into the script

The script runs three checks on every build:

1. **QuickSight cross-check** — parsed per-user sums equal `source_header_total - NaN_row_unattributed` for every dashboard × month. Unattributed events exist in the source but cannot be credited to any login; they flow through to the dashboard subtotal but not into any leader row.

2. **Cell-by-cell validation** — every data cell in the output sheet is compared to a direct source aggregation. 0 mismatches expected.

3. **Product vs avenue reconciliation** — for multi-avenue products, the product row total must equal the sum of its avenue rows across every month. Script prints any discrepancy.

## To re-run next month

1. Drop the four new source files into the Excel Analysis folder following the filename patterns above (change `YYYYMMDD` to the current date, keep `_v1` or bump).
2. Update the file path constants at the top of `scripts/build_integrated_rollup_v1.py`:
   - `OP`, `QS`, `TBU`, `TBV`, `HIER`
3. If QuickSight user-row ranges shift, update `QS_AXIS_ROWS` and `QS_CERBERUS_ROWS`.
4. Run: `python3 scripts/build_integrated_rollup_v1.py`
5. Review console output. All three validation checks should print no errors. If any mismatch prints, investigate before relying on the sheet.
6. Open the updated `usage metrics op_excellence_*.xlsx` and verify the `Product Rollup by L11` sheet.

## Known caveats

- **Unattributed QuickSight events.** The NaN-user row in the QuickSight crosstab represents events whose user isn't captured. These show up in source dashboard subtotals but not in any leader row because we can't map them to a manager chain. Typically small, but worth flagging if the gap grows.
- **Hierarchy gaps.** Any login in QuickSight or Tableau that is not present in the hierarchy lookup is dropped from the attribution. Check the `consolidated users` sheet: rows with `in_hierarchy = No` are the unresolvable users. Usually < 5% of the login base.
- **Duplicate manager names.** Some managers share the same name at the same level (e.g., two Jennifer Kim L8s). The script disambiguates by `manager_login`; a hidden `Login` column (Col E) in the output preserves the exact ID so validation is unambiguous.
- **Op Excellence distinct_users granularity.** The op_excellence source counts distinct users per (manager, week/month, product). When summing across products under a leader, users active in multiple products in the same month count once per product. This matches the source file's own native granularity; we do not attempt cross-product deduplication in op_excellence.
- **Dashboard-avenue distinct users are true cross-product distincts** within each source, computed from raw event-level data and attributed to every ancestor manager in the user's chain. This is more accurate than op_excellence's per-product counts.
- **Option C additive merge** means a user who accesses Axis via both op_excellence tooling and QuickSight Axis Monthly is counted in both avenues. That is by design — the metric answers "how many users per access path" not "distinct users across paths."
