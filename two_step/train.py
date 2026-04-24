import os
import warnings
import numpy as np
import pandas as pd
import librosa
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

BASE_PATHS = {"normal": "../data/normal", "abnormal": "../data/abnormal"}
MODEL_OUT = "model_bundle.pkl"

def extract_features(y, sr):
    if np.max(np.abs(y)) < 1e-4:
        y = y + 1e-6
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.concatenate([np.mean(mfcc, axis=1), np.std(mfcc, axis=1)])

records = []
for label, base_path in BASE_PATHS.items():
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(".wav"):
                y, sr = librosa.load(os.path.join(root, file), sr=None)
                records.append({
                    "features": extract_features(y, sr),
                    "binary": "normal" if label == "normal" else "abnormal"
                })

df = pd.DataFrame(records)
X = np.stack(df["features"].values)
y = df["binary"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

clf = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42, n_jobs=-1)
clf.fit(X_scaled, y)

scores = cross_val_score(clf, X_scaled, y, cv=StratifiedKFold(5, shuffle=True, random_state=42), scoring="f1_weighted")
print(scores.mean())

joblib.dump({"scaler": scaler, "clf": clf}, MODEL_OUT)