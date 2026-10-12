# Healthcare Analytics with Multi-Modal Data

**Open-data research platform: data engineering + tabular machine learning + image/VLM demonstrations + FastAPI + Streamlit + Docker + Azure infrastructure starter.**

> **Research and education only. Not a medical device; no diagnosis, triage, or treatment recommendations.** Tabular and image datasets represent **different, unrelated cohorts**. There is NO patient-level fusion or invented patient linkage.

## Architecture

```text
UCI Heart Disease (tabular) --> Bronze Parquet --> Silver Parquet --> Gold DuckDB analytics
                                        |                         |
                                        +--> sklearn research ML -> FastAPI score
MedMNIST PneumoniaMNIST images --> image metadata / optional BLIP generic caption -> FastAPI inspect
                                                                             |
                                                                   Streamlit web frontend

Docker Compose: FastAPI + Streamlit
CI: GitHub Actions tests + Docker build
Azure roadmap: ADLS Gen2 -> Databricks Delta -> Container Apps -> Monitor / Foundry vision
```

## Open-source datasets

1. **UCI Heart Disease** (303 Cleveland rows among collections; real historical research data; CC BY 4.0): https://archive.ics.uci.edu/dataset/45/heart+disease — downloaded with `ucimlrepo`.
2. **MedMNIST PneumoniaMNIST** (5,856 preprocessed pediatric chest radiograph images; CC BY 4.0): https://medmnist.com/ — downloaded with `medmnist`.

Datasets are obtained by script, not copied to this public repository. Images and clinical data must **not** be joined as though they came from the same patients. See [data provenance](docs/data-sources.md).

## Run locally (Windows PowerShell)

```powershell
git clone https://github.com/Khadija162/Healthcare-Analytics-with-Multi-Modal-Data.git
cd Healthcare-Analytics-with-Multi-Modal-Data
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m healthcare.data --dataset heart
.\.venv\Scripts\python.exe -m healthcare.etl
.\.venv\Scripts\python.exe -m healthcare.train
.\.venv\Scripts\python.exe -m pytest -q
```

Download separate image benchmark (optional):

```powershell
.\.venv\Scripts\python.exe -m healthcare.data --dataset pneumonia
```

Start API and frontend in separate terminals:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

- FastAPI docs: http://127.0.0.1:8000/docs
- Streamlit dashboard: http://localhost:8501

### Docker

After running training:

```powershell
docker compose up --build
```

Default image endpoint performs only pixel/metadata inspection. For an **optional generic BLIP caption model**, install PyTorch/transformers separately and configure `VLM_MODE=blip`; this downloads model weights and is **not** radiology interpretation.

## Project layout

- `healthcare/data.py`: public dataset downloads
- `healthcare/etl.py`: Bronze, Silver, Gold Parquet + DuckDB
- `healthcare/train.py`: baseline research ML with metrics
- `healthcare/vlm.py`: image inspection and optional open-weight captioning
- `backend/main.py`: FastAPI heart score and image endpoints
- `dashboard/app.py`: Streamlit frontend
- `tests/`: API/image unit tests
- `infra/terraform/`: example Azure Resource Group + ADLS Gen2 (not deployed)
- `docs/`: provenance, privacy and target architecture

## Implementation status and limitations

**Committed starter code**; live training success, cloud services, and deployment have not yet been independently verified. The original datasets are not paired; this is a platform showing two data modalities, not actual fused clinical predictions. The clinical scoring baseline is tiny and subject to bias, calibration issues, leakage risks and dataset shift. Do not expose the unauthenticated API publicly.

Planned: Azure Databricks/Delta pipelines, secure Azure Container Apps, Entra ID/Key Vault, monitoring with Azure Monitor, and a properly evaluated licensed VLM deployment. No Azure resources were created here.
