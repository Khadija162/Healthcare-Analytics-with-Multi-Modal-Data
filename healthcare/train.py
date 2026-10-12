"""Baseline research classification with imputation inside CV-safe train/test pipeline."""
import argparse
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from healthcare.etl import FEATURES

def train(path="data/raw/heart.csv", output="artifacts/heart_model.joblib"):
    frame=pd.read_csv(path,na_values=["?"])
    missing=set(FEATURES+["target"])-set(frame.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    target=pd.to_numeric(frame["target"],errors="coerce")
    frame=frame.loc[target.notna()].copy()
    y=(target.loc[frame.index]>0).astype(int)
    x=frame[FEATURES].apply(pd.to_numeric,errors="coerce")
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.25,stratify=y,random_state=42)
    pipe=Pipeline([("transform",ColumnTransformer([("all",Pipeline([
        ("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),FEATURES)])),
        ("model",LogisticRegression(max_iter=500))])
    pipe.fit(x_train,y_train)
    scores=pipe.predict_proba(x_test)[:,1]
    metrics={"dataset":"UCI Heart Disease, separate from MedMNIST images",
       "train_rows":len(x_train),"test_rows":len(x_test),
       "roc_auc":float(roc_auc_score(y_test,scores)),
       "average_precision":float(average_precision_score(y_test,scores)),
       "evaluation_limitations":"Single random holdout; research-only, not validated clinically"}
    targetpath=Path(output);targetpath.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(pipe,targetpath)
    targetpath.with_suffix(".metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    return metrics

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--csv",default="data/raw/heart.csv")
    a=p.parse_args();print(json.dumps(train(a.csv),indent=2))
