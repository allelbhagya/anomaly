import streamlit as st
import numpy as np
import librosa
import joblib
import tempfile
import os
import warnings

st.set_page_config(page_title="AudioDx", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0d0d0d; }
[data-testid="stFileUploader"] { background: #161616 !important; border: 1px dashed #333 !important; border-radius: 8px !important; }
.stButton > button { background: #fff !important; color: #000 !important; border: none !important; border-radius: 6px !important; font-weight: 600 !important; width: 100%; }
.tag { display: inline-block; margin-top: 1.5rem; padding: 0.6rem 1.2rem; border-radius: 6px; font-family: monospace; font-size: 1rem; font-weight: 700; }
.normal { background: #0f2b1a; color: #4ade80; border: 1px solid #166534; }
.abnormal { background: #2b0f0f; color: #f87171; border: 1px solid #991b1b; }
.conf { font-family: monospace; font-size: 0.8rem; color: #555; margin-top: 0.4rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("### audio check")

@st.cache_resource
def load_model():
    if not os.path.exists("model_bundle.pkl"):
        return None
    return joblib.load("model_bundle.pkl")

def extract_features(y, sr):
    if np.max(np.abs(y)) < 1e-4:
        y = y + 1e-6
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.concatenate([np.mean(mfcc, axis=1), np.std(mfcc, axis=1)])

bundle = load_model()
if bundle is None:
    st.error("model_bundle.pkl not found. Run train.py first.")
    st.stop()

uploaded = st.file_uploader("Upload a WAV file", type=["wav"], label_visibility="collapsed")

if uploaded:
    st.audio(uploaded, format="audio/wav")
    if st.button("Analyse"):
        with st.spinner("processing"):
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name
            try:
                y_audio, sr = librosa.load(tmp_path, sr=None)
            finally:
                os.unlink(tmp_path)

            X = bundle["scaler"].transform(extract_features(y_audio, sr).reshape(1, -1))
            proba = bundle["clf"].predict_proba(X)[0]
            classes = list(bundle["clf"].classes_)
            normal_conf = proba[classes.index("normal")]
            abnormal_conf = proba[classes.index("abnormal")]
            pred = "normal" if normal_conf > abnormal_conf else "abnormal"
            conf = normal_conf if pred == "normal" else abnormal_conf

        st.markdown(f'<div class="tag {pred}">{"NORMAL" if pred == "normal" else "ABNORMAL"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="conf">confidence {conf*100:.1f}%</div>', unsafe_allow_html=True)