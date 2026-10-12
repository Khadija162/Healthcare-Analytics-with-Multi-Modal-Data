"""Bronze/Silver/Gold clinical-tabular ETL; preserves provenance, never claims cohort linkage."""
import argparse
from pathlib import Path
import duckdb
import pandas as pd

FEATURES=["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"]
def build(source="data/raw/heart.csv",root="data"):
    df=pd.read_csv(source,na_values=["?"])
    missing=set(FEATURES+["target"])-set(df.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    root=Path(root)
    for layer in ("bronze","silver","gold"): (root/layer).mkdir(parents=True,exist_ok=True)
    df.to_parquet(root/"bronze"/"heart.parquet",index=False)
    target=pd.to_numeric(df["target"],errors="coerce")
    valid=target.between(0,4)&pd.to_numeric(df["age"],errors="coerce").between(0,120)
    clean=df.loc[valid].copy()
    clean["heart_disease"]=(target.loc[valid]>0).astype(int)
    clean.to_parquet(root/"silver"/"heart.parquet",index=False)
    conn=duckdb.connect()
    try:
        conn.execute("CREATE OR REPLACE VIEW heart AS SELECT * FROM read_parquet(?)",[str((root/"silver"/"heart.parquet").as_posix())])
        summary=conn.execute("SELECT heart_disease, COUNT(*) AS records, AVG(age) AS avg_age FROM heart GROUP BY heart_disease ORDER BY heart_disease").df()
        summary.to_parquet(root/"gold"/"heart_summary.parquet",index=False)
    finally: conn.close()
    return {"bronze":int(len(df)),"silver":int(len(clean)),"rejected":int((~valid).sum()),"gold_groups":int(len(summary))}

if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--csv",default="data/raw/heart.csv")
    args=a.parse_args();print(build(args.csv))
