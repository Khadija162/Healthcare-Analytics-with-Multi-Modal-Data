"""Fetch open UCI Heart Disease data and MedMNIST images; NO patient-level linkage."""
import argparse
from pathlib import Path
import pandas as pd

def heart(output="data/raw/heart.csv"):
    from ucimlrepo import fetch_ucirepo
    data = fetch_ucirepo(id=45)
    features = data.data.features.copy()
    targets = data.data.targets.copy()
    targets.columns = ["target"]
    frame = pd.concat([features.reset_index(drop=True), targets.reset_index(drop=True)], axis=1)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return str(path), len(frame)

def pneumonia(output="data/medmnist"):
    from medmnist import PneumoniaMNIST
    ds = PneumoniaMNIST(split="train", root=output, download=True)
    return {"train_images": len(ds), "path": output}

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",choices=["heart","pneumonia"],default="heart")
    a=p.parse_args()
    print(heart() if a.dataset=="heart" else pneumonia())
