# NCA Construction Analytics Platform
### Sector data platform · National Construction Authority, Kenya · 2023–2025

Data work I led at the National Construction Authority: 11 years (2014–2025) of construction-sector data across all 47 counties, automated ETL feeding Power BI and the NCA Research Portal, and research models (MSME mechanisation, affordable-housing productivity, BIM uptake).

- API-integrated Power BI dashboards **cut reporting time by 60%**
- Standardised and deduplicated contractor data across 47 counties
- Trained 160+ contractors and researchers in analytics, SPSS, Excel and Power BI

NCA data is proprietary and not published. `python/demo_county_etl.py` shows the ETL pattern on **synthetic data**.

## Run the demo
```bash
pip install -r requirements.txt
python python/demo_county_etl.py
```
It standardises messy county names to the 47 official counties, drops unmapped rows and duplicates, reports a data-quality summary, and writes a county × year KPI table (contractors, turnover, top-grade share, YoY growth) that a Power BI report can read.

## Related
[MSME Mechanisation Framework](https://github.com/amosmuthomi-tech/msme-mechanisation-framework)

`Power BI` `SQL` `Python` `R` `SPSS` `ETL`
