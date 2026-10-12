import streamlit as st

CSS_CHAMPS = """
<style>
[data-testid="stWidgetLabel"] p {font-weight:700 !important; font-size:1.02rem !important; letter-spacing:.2px}
.stTextInput [data-baseweb="input"], .stNumberInput [data-baseweb="input"], .stTextArea [data-baseweb="textarea"],
.stDateInput [data-baseweb="input"], [data-baseweb="select"] > div {
    background:#ffffff !important; border:2px solid #4fae7b !important; border-radius:12px !important;
    box-shadow:0 3px 10px rgba(0,0,0,.18) !important; min-height:46px; transition:all .2s}
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input,
[data-baseweb="select"] div, [data-baseweb="select"] span {color:#12312a !important; font-size:1.05rem !important; background-color:transparent !important}
.stTextInput input::placeholder {color:#7a8f88 !important}
[data-baseweb="select"] svg {fill:#12312a !important}
.stTextInput [data-baseweb="input"]:focus-within, .stNumberInput [data-baseweb="input"]:focus-within,
.stTextArea [data-baseweb="textarea"]:focus-within, [data-baseweb="select"] > div:focus-within {
    border-color:#d4af37 !important; box-shadow:0 0 0 4px rgba(212,175,55,.35) !important}
[data-testid="stForm"] {border:2px solid rgba(212,175,55,.55) !important; border-radius:18px !important; padding:24px !important; background:rgba(255,255,255,.05)}
[data-testid="stExpander"] {border:2px solid rgba(212,175,55,.5) !important; border-radius:16px !important; background:rgba(255,255,255,.04)}
[data-testid="stExpander"] summary p {font-weight:700 !important; font-size:1.1rem !important}
[data-testid="stFileUploaderDropzone"] {background:rgba(79,174,123,.14) !important; border:2px dashed #4fae7b !important; border-radius:16px !important; padding:22px}
[data-testid="stFileUploaderDropzone"] button {border:1.5px solid #d4af37 !important; border-radius:999px !important; font-weight:700}
[data-testid="stDataFrame"] {border:2px solid rgba(212,175,55,.45); border-radius:14px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,.25)}
</style>
"""


def appliquer_champs():
    st.markdown(CSS_CHAMPS, unsafe_allow_html=True)
