# Hospital Operations Dashboard (Power BI)

**Problem:** Hospital leadership needs one view of volume, capacity, quality,
and cost — but the data lives in disconnected operational reports.

**Approach:** A 3-page Power BI executive dashboard on a synthetic
12,236-admission dataset (2024–2026): KPI cards for at-a-glance health, trend
lines for trajectory, and department/payer breakdowns for root-cause digging.

## Key findings (from the data)

| KPI | Value |
|-----|-------|
| Total admissions | **12,236** |
| Average length of stay | **4.6 days** |
| 30-day readmission rate | **10.1%** |
| Total charges | **$229M** |
| Busiest department | **Emergency** (2,121 admissions) |
| Largest payer | **Private Insurance** (38%), then Medicare (34%) |

## What's in this repo

| Path | Contents |
|------|----------|
| `data/` | Synthetic `admissions.csv` (12,236 rows), `patients.csv`, `departments.csv` + the seeded generator — **no real patient data** |
| `powerbi/DAX_measures.dax` | 12 production-style measures: volume, LOS, occupancy, readmissions, financials, MoM/YTD time intelligence |
| `powerbi/date_table_m.pq` | Power Query (M) date dimension — paste into a Blank Query |
| `powerbi/data_model.md` | Star-schema diagram, relationships, and data dictionary |
| `docs/BUILD_GUIDE.md` | Step-by-step: CSVs → model → measures → 3 finished pages in ~30 minutes |
| `assets/wireframe.html` | Layout wireframes for all 3 pages (open in a browser) |

## Dashboard pages

1. **Executive Overview** — KPI cards, admissions trend, admissions by department, payer-mix donut
2. **Patient Flow & Capacity** — bed occupancy % vs 85% target, avg daily census, LOS by department, weekday heatmap
3. **Quality & Readmissions** — readmission KPIs, rate by department, trend, diagnosis detail table

## Build the .pbix

Power BI Desktop is required for the final assembly (this repo contains
everything around it). Follow [`docs/BUILD_GUIDE.md`](docs/BUILD_GUIDE.md),
save as `powerbi/hospital-ops-dashboard.pbix`, and commit it here.

## Skills demonstrated

Power BI (data modeling, DAX, Power Query M) · star-schema design · KPI design
for healthcare operations · translating business questions into dashboard pages
