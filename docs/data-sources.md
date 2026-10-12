# Open-source data and provenance

## UCI Heart Disease (tabular)
- Official: https://archive.ics.uci.edu/dataset/45/heart+disease
- DOI: 10.24432/C52P4X
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Original creators: Andras Janosi, William Steinbrunn, Matthias Pfisterer, Robert Detrano
- Acquisition: `python -m healthcare.data --dataset heart`; cached under ignored `data/raw/`.
- UCI source contains historical clinical data; treat as sensitive research information even though identifiers have been replaced. Not validated for modern clinical practice.

## MedMNIST PneumoniaMNIST (images)
- Official: https://medmnist.com/
- Code/info: https://github.com/MedMNIST/MedMNIST
- License for PneumoniaMNIST: CC BY 4.0, with attribution to original dataset and MedMNIST paper.
- Acquisition: `python -m healthcare.data --dataset pneumonia`; cached under ignored `data/medmnist/`.
- PneumoniaMNIST is image classification research data. The example VLM uses a *generic image captioner*, not a radiology model, and its output does not diagnose pneumonia.

**The datasets are unrelated and have no patient-level join key.** This repository demonstrates *multimodal infrastructure*, not actual per-patient multimodal fusion. Never fabricate patient matches or infer diagnoses from combined outputs.

No third-party patient records or image files are committed in this repository. Respect research data licenses, source attribution and applicable privacy policies.
