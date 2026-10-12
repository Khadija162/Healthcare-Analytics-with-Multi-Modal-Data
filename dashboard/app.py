"""Research operations dashboard; demonstrates unpaired data modalities."""
import os
from pathlib import Path
import streamlit as st
import requests
st.set_page_config(page_title="Multimodal Healthcare Research",layout="wide")
st.title("Healthcare Analytics · Multimodal Research")
st.warning("Educational research demo only. Not for diagnosis, treatment or clinical decision-making.")
api=os.getenv("API_URL","http://127.0.0.1:8000")
a,b=st.tabs(["Tabular analytics","Image / VLM research"])
with a:
    st.write("UCI Heart Disease benchmark is independent of the image dataset.")
    if Path("data/gold/heart_summary.parquet").exists():
        import pandas as pd
        st.dataframe(pd.read_parquet("data/gold/heart_summary.parquet"))
    else: st.info("Run Python ETL first to populate Gold analytics.")
with b:
    st.write("Upload a synthetic or public benchmark image. No patient identifying information.")
    picture=st.file_uploader("Image",type=["png","jpg","jpeg","webp"])
    if picture and st.button("Inspect image"):
        try:
            r=requests.post(api+"/api/images/inspect",files={"file":(picture.name,picture.getvalue(),picture.type)},timeout=120)
            if r.ok:st.json(r.json())
            else:st.error(f"HTTP {r.status_code}: {r.text}")
        except requests.RequestException as e:st.error(str(e))
st.caption("Images and tabular rows are separate datasets. No patient-level fusion is claimed.")
