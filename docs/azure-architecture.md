# Azure data engineering + AI/VLM roadmap

## Implemented locally
- UCI Heart Disease ingestion, Parquet Bronze/Silver/Gold pipeline, DuckDB Gold SQL
- Research-only logistic regression model with imputation
- FastAPI tabular scoring endpoint and image inspection endpoint
- Streamlit tabular and image demonstration
- Optional **BLIP generic image captioning** behind `VLM_MODE=blip` using installed transformers/torch; no diagnosis
- Docker Compose, GitHub Actions, Terraform ADLS Gen2 starting point

## Target Azure deployment (NOT provisioned)
UCI/MedMNIST ingestion -> ADLS Gen2 Bronze -> Azure Databricks PySpark/Delta Silver/Gold -> Azure Database for PostgreSQL metrics -> FastAPI Container Apps -> dashboard Container Apps or Static Web Apps. Use Azure Monitor, App Insights and Key Vault; Microsoft Entra ID for authorization. VLM inference may use Foundry-hosted supported vision model or a managed GPU with a tested open-source VLM and model-specific licenses.

## Guardrails
Only publicly licensed, de-identified or synthetic benchmark data. No actual patient uploads into public demos, no diagnostic inference, no autonomous recommendations for treatment. Model should refuse clinical decision requests. Encrypt data, add auth and audit logs before deployment. Use role-based access and minimize retained images and prompts.

Terraform here does not provision the entire platform. Applying it may incur Azure costs.
