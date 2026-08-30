"""Real-world benchmark dataset loaders.

The benchmark suite uses public datasets with explicit provenance.
Downloads happen only when the benchmark runner is invoked.
"""

from pathlib import Path
import io
import urllib.request
import zipfile

import numpy as np
import pandas as pd
from scipy.io import arff
from sklearn.datasets import fetch_kddcup99, load_breast_cancer as sklearn_load_breast_cancer


DATA_DIR = Path(__file__).resolve().parent / "data"


def load_website_phishing():
    """UCI Website Phishing (dataset 379).

    The UCI target encodes Legitimate=1, Suspicious=0, Phishy=-1.
    For anomaly detection we evaluate only the unambiguous classes:
    Legitimate -> 0 (normal), Phishy -> 1 (anomaly).
    Suspicious rows are excluded.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = DATA_DIR / "website_phishing.zip"
    url = "https://archive.ics.uci.edu/static/public/379/website+phishing.zip"

    if not archive_path.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            archive_path.write_bytes(response.read())

    with zipfile.ZipFile(archive_path) as archive:
        arff_name = next(name for name in archive.namelist() if name.lower().endswith(".arff"))
        raw = archive.read(arff_name)

    data, _ = arff.loadarff(io.BytesIO(raw))
    df = pd.DataFrame(data)
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(
                lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
            )

    target = "Result"
    df[target] = pd.to_numeric(df[target], errors="coerce")
    df = df[df[target].isin([-1, 1])].copy()
    df[target] = (df[target] == -1).astype(int)

    return df, {
        "name": "UCI Website Phishing",
        "source": "UCI Machine Learning Repository, dataset 379",
        "citation": "Abdelhamid et al. (2014), DOI 10.24432/C5B301",
        "label_mapping": "Legitimate=0 normal; Phishy=-1 anomaly; Suspicious excluded",
    }


def load_kddcup99(sample_size=20000, random_state=42):
    """KDD Cup 1999 via scikit-learn's public dataset loader.

    Normal traffic is 0; every attack category is 1.
    A reproducible stratified sample is used for practical local benchmarking.
    """
    data = fetch_kddcup99(subset=None, shuffle=True, random_state=random_state, percent10=True)
    X = pd.DataFrame(data.data)
    y = pd.Series(data.target).astype(str).str.strip()

    # Decode bytes and one-hot encode categorical columns.
    X = X.map(lambda v: v.decode("utf-8") if isinstance(v, bytes) else v)
    X = pd.get_dummies(X, drop_first=False)
    y_binary = (y != "b'normal.'").astype(int)

    df = X.copy()
    df["label"] = y_binary.to_numpy()

    if sample_size and len(df) > sample_size:
        # Preserve class proportions deterministically.
        from sklearn.model_selection import train_test_split
        sample, _ = train_test_split(
            df,
            train_size=sample_size,
            stratify=df["label"],
            random_state=random_state,
        )
        df = sample.reset_index(drop=True)

    return df, {
        "name": "KDD Cup 1999 (10% subset)",
        "source": "KDD Cup 1999, accessed through scikit-learn fetch_kddcup99",
        "citation": "KDD Cup 1999 Data",
        "label_mapping": "normal.=0 normal; all attack classes=1 anomaly",
    }



def load_breast_cancer():
    """Real-world UCI Breast Cancer dataset bundled with scikit-learn.

    This is a proxy anomaly benchmark: malignant cases are treated as
    anomalies and benign cases as normal. The mapping is explicit because
    the original dataset is a supervised classification dataset, not an
    anomaly-detection dataset.
    """
    data = sklearn_load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    # sklearn target: 0 malignant, 1 benign.
    df["label"] = (data.target == 0).astype(int)
    return df, {
        "name": "Breast Cancer Wisconsin (Diagnostic)",
        "source": "UCI Machine Learning Repository via scikit-learn",
        "citation": "Street, W.N., Wolberg, W.H., Mangasarian, O.L. (1993)",
        "label_mapping": "Malignant=1 anomaly; Benign=0 normal (proxy anomaly benchmark)",
    }


DATASET_LOADERS = {
    "website_phishing": load_website_phishing,
    "kddcup99": load_kddcup99,
    "breast_cancer": load_breast_cancer,
}
