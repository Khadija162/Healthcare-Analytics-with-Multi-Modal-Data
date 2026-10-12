"""Local-only research API; NO clinical use. No authentication; never deploy publicly as-is."""
import os
from functools import lru_cache
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI,HTTPException,UploadFile,File
from pydantic import BaseModel,ConfigDict,Field
from healthcare.etl import FEATURES
from healthcare.vlm import inspect_image
app=FastAPI(title="Multimodal Healthcare Research Platform",version="0.1.0")
class HeartFeatures(BaseModel):
    model_config=ConfigDict(extra="forbid")
    age:float=Field(ge=0,le=120)
    sex:float;cp:float;trestbps:float;chol:float;fbs:float;restecg:float
    thalach:float;exang:float;oldpeak:float;slope:float;ca:float;thal:float
@lru_cache(maxsize=1)
def model():
    p=Path(os.getenv("MODEL_PATH","artifacts/heart_model.joblib"))
    if not p.is_file(): raise FileNotFoundError("Train model first")
    return joblib.load(p) # Trusted artifacts only
@app.get("/health")
def health():
    return {"status":"ok","model_ready":Path(os.getenv("MODEL_PATH","artifacts/heart_model.joblib")).is_file()}
@app.post("/api/heart/score")
def score(input:HeartFeatures):
    try: m=model()
    except FileNotFoundError as exc: raise HTTPException(503,str(exc)) from exc
    frame=pd.DataFrame([input.model_dump()])[FEATURES]
    probability=float(m.predict_proba(frame)[0,1])
    return {"research_probability":round(probability,5),"notice":"Not a diagnosis or treatment recommendation"}
@app.post("/api/images/inspect")
async def image_inspect(file:UploadFile=File(...)):
    if file.content_type not in ("image/png","image/jpeg","image/webp"):
        raise HTTPException(415,"Only PNG/JPEG/WebP supported")
    raw=await file.read(5_000_001)
    try: return inspect_image(raw)
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    except RuntimeError as exc: raise HTTPException(503,str(exc)) from exc
