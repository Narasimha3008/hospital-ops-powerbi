# Build guide — from CSVs to finished .pbix in ~30 minutes

Follow these steps in Power BI Desktop. The wireframe for each page is in
`assets/wireframe.html` (open in any browser) — build each page to match it.

## Part 1 — Load the data (5 min)

1. **Get Data > Text/CSV** and load, in order:
   - `data/admissions.csv`
   - `data/patients.csv`
   - `data/departments.csv`
2. In Power Query, for the **Admissions** table set types:
   - `admission_date`, `discharge_date` → **Date**
   - `length_of_stay` → **Whole Number**
   - `total_charges` → **Decimal Number**
   - `readmitted_30d` → **TRUE/FALSE** (logical)
3. **New Source > Blank Query > Advanced Editor**: paste the full contents of
   `powerbi/date_table_m.pq`. Rename the query to `Date`.
4. **Close & Apply.**

## Part 2 — Model (5 min)

1. Open **Model view**. Create the three relationships from
   `powerbi/data_model.md` (all Many-to-one, Single direction):
   - `Admissions[patient_id]` → `Patients[patient_id]`
   - `Admissions[department]` → `Departments[department]`
   - `Admissions[admission_date]` → `Date[Date]`
2. Right-click the `Date` table > **Mark as date table** > choose `Date[Date]`.
3. Hide raw key columns you won't slice by (`admission_id`, `patient_id` on the
   fact table) to keep the field list clean.

## Part 3 — Measures (5 min)

1. Select the **Admissions** table > **New measure**.
2. Paste each measure from `powerbi/DAX_measures.dax` one at a time.
3. Format: `Readmission Rate` and `Bed Occupancy %` → **%**; `Total Charges` →
   **$**; `Admissions MoM %` → **%**.

## Part 4 — Report pages (15 min)

Apply the slicers **once per page** (or use Sync Slicers across pages):
`Date[Year]`, `Date[Month]`, `Departments[department]`, `Admissions[payer]`.

### Page 1 — Executive Overview
| Visual | Fields |
|--------|--------|
| 4 KPI cards | `Total Admissions`, `Avg Length of Stay`, `Readmission Rate`, `Total Charges` |
| Line chart | Axis: `Date[MonthYear]` (sort by `Date[Year]`, `Date[MonthNumber]`) · Values: `Total Admissions`, `Admissions YTD` |
| Bar chart | Y: `Departments[department]` · X: `Total Admissions` |
| Donut chart | Legend: `Admissions[payer]` · Values: `Charges % of Total` |

### Page 2 — Patient Flow & Capacity
| Visual | Fields |
|--------|--------|
| Bar chart | Y: `Departments[department]` · X: `Bed Occupancy %` · target line at 85% (Analytics pane) |
| Line chart | Axis: `Date[MonthYear]` · Values: `Avg Daily Census` |
| Bar chart | Y: `Departments[department]` · X: `Avg Length of Stay` |
| Matrix | Rows: `Date[DayName]` · Columns: `Date[Month]` · Values: `Total Admissions` (conditional formatting → heatmap) |

### Page 3 — Quality & Readmissions
| Visual | Fields |
|--------|--------|
| KPI cards | `Readmissions (30-day)`, `Readmission Rate` |
| Bar chart | Y: `Departments[department]` · X: `Readmission Rate` |
| Line chart | Axis: `Date[MonthYear]` · Values: `Readmission Rate` |
| Table | `Admissions[diagnosis]`, `Total Admissions`, `Avg Length of Stay`, `Avg Charges per Admission`, `Readmission Rate` — sorted by `Total Admissions` desc |

**Formatting pass:** View > Themes (pick one and stick to it), give every visual
a title, turn on Data labels for cards, and add a text box on Page 1 with the
data-as-of date. Keep it to 3 pages — executives stop scrolling after that.

## Part 5 — Save & publish

1. Save as `hospital-ops-dashboard.pbix` in this repo's `powerbi/` folder.
2. Commit and push — the repo README already documents the KPIs, so the .pbix
   completes the story.

## Troubleshooting

- **Time-intelligence measures return blank** → the Date table isn't marked as
  a date table, or there's a gap in the relationship to `admission_date`.
- **Bed Occupancy % looks wrong** → check that the Departments relationship
  filters `beds` (Single direction, no bi-directional filtering needed).
- **MonthYear sorts alphabetically** → in Data view, select `MonthYear` >
  **Sort by column** > `MonthNumber` won't work across years; instead sort the
  axis by `Date[Date]` or use Year + MonthNumber in the visual.
