"""County-level ETL + KPI demo on SYNTHETIC data (NCA data is proprietary and not published).

Shows the pattern: merge sources -> standardise 47 county names -> deduplicate ->
quality-score -> KPI table ready for Power BI.
"""
import numpy as np, pandas as pd

COUNTIES = ["Mombasa","Kwale","Kilifi","Tana River","Lamu","Taita-Taveta","Garissa","Wajir","Mandera","Marsabit","Isiolo","Meru",
 "Tharaka-Nithi","Embu","Kitui","Machakos","Makueni","Nyandarua","Nyeri","Kirinyaga","Murang'a","Kiambu","Turkana","West Pokot",
 "Samburu","Trans-Nzoia","Uasin Gishu","Elgeyo-Marakwet","Nandi","Baringo","Laikipia","Nakuru","Narok","Kajiado","Kericho","Bomet",
 "Kakamega","Vihiga","Bungoma","Busia","Siaya","Kisumu","Homa Bay","Migori","Kisii","Nyamira","Nairobi"]


def make_raw(seed=5, n=6000):
    r = np.random.default_rng(seed)
    dirty = [c.upper() if r.random() < .15 else c.lower() if r.random() < .15 else c + " " for c in r.choice(COUNTIES, n)]
    df = pd.DataFrame({"contractor_id": r.integers(1, 4000, n), "county": dirty, "year": r.integers(2014, 2026, n),
                       "grade": r.choice(["NCA1", "NCA2", "NCA3", "NCA4", "NCA5"], n),
                       "turnover_m": r.lognormal(2, 1, n).round(2)})
    df.loc[r.choice(n, 120, replace=False), "county"] = None  # missing values
    return pd.concat([df, df.sample(300, random_state=1)])  # duplicates


def clean(df):
    lookup = {c.lower(): c for c in COUNTIES}
    out = df.copy()
    out["county_std"] = out["county"].str.strip().str.lower().map(lookup)
    q = {"rows_in": len(out), "unmapped_county": int(out["county_std"].isna().sum())}
    out = out.dropna(subset=["county_std"]).drop_duplicates(["contractor_id", "county_std", "year"])
    q["rows_out"] = len(out)
    q["completeness_pct"] = round(100 * q["rows_out"] / q["rows_in"], 1)
    return out, q


def kpis(df):
    k = df.groupby(["county_std", "year"]).agg(contractors=("contractor_id", "nunique"), turnover_m=("turnover_m", "sum"),
                                              top_grade_share=("grade", lambda s: (s.isin(["NCA1", "NCA2"])).mean())).reset_index()
    k["contractors_yoy"] = k.sort_values("year").groupby("county_std")["contractors"].pct_change()
    return k


if __name__ == "__main__":
    clean_df, q = clean(make_raw())
    k = kpis(clean_df)
    print("quality:", q, "| counties:", k.county_std.nunique(), "| years:", k.year.min(), "-", k.year.max())
    print(k.head(6).round(2).to_string(index=False))
    k.to_csv("county_kpis_demo.csv", index=False)
