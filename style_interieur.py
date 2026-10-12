import base64
from pathlib import Path

import seaborn as sns
import streamlit as st

DOSSIER = Path(__file__).parent / "images"
OR = "#d4af37"
BLEU = "#0f3d6e"
ENCRE = "#1b2a3a"
SITE_PHOTOS = ["slide6.jpg", "slide7.jpg"]  # photos des cartes de sites (alternees)
PHOTO_CARTE2 = "slide5.jpg"  # photo de la carte caracteristiques
PHOTO_CARTE = "slide4.jpg"   # photo de fond de la carte description (dossier images)
PALETTE = ["#6B8FB5", "#4C9F7A", "#d4af37", "#7fb3d5", "#e0975a", "#64748b"]

_HEX_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'>"
            "<g fill='#eef1f7'><polygon points='30,10 52,22 52,46 30,58 8,46 8,22'/>"
            "<polygon points='72,34 94,46 94,70 72,82 50,70 50,46'/>"
            "<polygon points='30,58 52,70 52,94 30,106 8,94 8,70'/></g></svg>")
HEX = "data:image/svg+xml;base64," + base64.b64encode(_HEX_SVG.encode()).decode()


@st.cache_resource
def _b64(nom):
    return base64.b64encode((DOSSIER / nom).read_bytes()).decode()


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Saira:wght@400;600;700&display=swap');
.stApp {background:#f4f6fa !important}
[data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container {background:transparent !important}
[data-testid="stHeader"] {background:rgba(255,255,255,.92); backdrop-filter:blur(6px)}
.block-container {padding-top:2.5rem !important}
h1, h2, h3, .stTabs [data-baseweb="tab"] {font-family:'Saira',sans-serif !important}
h1, h2, h3 {color:#0f3d6e !important}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#0f3d6e,#0b5a56) !important; border-right:none}
[data-testid="stSidebar"] * {color:#fff}
.stTabs [data-baseweb="tab-list"] {gap:10px; border-bottom:none !important; background:#fff; border-radius:12px; padding:10px 14px; margin-bottom:14px; box-shadow:0 6px 18px rgba(15,61,110,.10); flex-wrap:wrap}
.stTabs [data-baseweb="tab"] {font-family:'Saira',sans-serif !important; height:auto; background:#fff; border:1.5px solid #d5dbe6; border-radius:999px; padding:10px 22px; margin:0;
    box-shadow:0 4px 12px rgba(15,61,110,.08); transition:all .2s; cursor:pointer}
.stTabs [data-baseweb="tab"] p {color:#0f3d6e !important; font-weight:700; font-size:1rem; letter-spacing:.3px}
.stTabs [data-baseweb="tab"]:hover {background:#e6f6ef; border-color:#059669; transform:translateY(-2px); box-shadow:0 8px 18px rgba(5,150,105,.18)}
.stTabs [aria-selected="true"] {background:#059669 !important; border-color:#059669 !important; box-shadow:0 8px 18px rgba(5,150,105,.32)}
.stTabs [aria-selected="true"] p {color:#fff !important}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {display:none !important}
[data-testid="stSelectbox"] {max-width:300px}
[class*="st-key-carte"] {background:#fff; border:1px solid #e3e8f0; border-radius:8px; padding:18px 20px; margin-bottom:18px; box-shadow:0 8px 22px rgba(15,61,110,.08)}
[class*="st-key-carte"] [class*="st-key-carte"] {background:none; border:none; box-shadow:none; padding:0; margin:0}
.stButton button, .stDownloadButton button {border-radius:999px; border:1.5px solid #059669; color:#059669; font-weight:700; transition:all .2s}
.stButton button:hover, .stDownloadButton button:hover {background:#059669; color:#fff; transform:translateY(-2px)}
[data-testid="stMetric"] {background:#fff; border:1px solid #e3e8f0; border-left:5px solid #059669; border-radius:10px; padding:14px 16px;
                          box-shadow:0 8px 22px rgba(15,61,110,.08)}
.hero2 {position:relative; height:430px; border-radius:16px; overflow:hidden; border-bottom:4px solid #d4af37;
         box-shadow:0 14px 40px rgba(15,61,110,.28); margin-bottom:26px}
.hero2 .bg {position:absolute; inset:0; background-size:cover; background-position:center; animation:zoomh 22s ease-in-out infinite alternate}
.hero2 .vl {position:absolute; inset:0; background:linear-gradient(100deg,rgba(8,34,72,.92) 10%,rgba(10,70,92,.60) 55%,rgba(16,185,129,.18) 100%)}
.hero2 .in {position:absolute; inset:0; padding:44px 52px; display:flex; flex-direction:column; justify-content:center; z-index:2}
.hero2 .eb {align-self:flex-start; background:rgba(212,175,55,.15); border:1px solid #d4af37; color:#f3d774; font-size:14px; font-weight:700; letter-spacing:2px; padding:6px 14px; border-radius:999px}
.hero2 .t {font-family:'Saira',sans-serif; color:#fff !important; font-size:58px; font-weight:700; line-height:1.05; margin:18px 0 12px; text-shadow:0 3px 16px rgba(0,0,0,.5); animation:monte .9s ease both}
.hero2 .s {color:#e6eefb; font-size:22px; font-weight:600; letter-spacing:.5px}
.hero2 .pills {display:flex; gap:14px; margin-top:26px; flex-wrap:wrap}
.hero2 a.pill, .hero2 span.pill {background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.6); color:#fff !important;
    padding:9px 20px; border-radius:24px; font-size:16px; text-decoration:none !important; backdrop-filter:blur(4px); transition:all .2s}
.hero2 a.pill:hover {background:#fff; color:#0f3d6e !important; border-color:#fff}
.hero2 img.badge {position:absolute; top:26px; right:36px; width:100px; height:112px; padding:6px; background:#fff; object-fit:cover; z-index:3;
    clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)}
.kpis {display:grid; grid-template-columns:repeat(4,1fr); gap:22px; margin:8px 0 26px}
.kpi {font-family:'Saira',sans-serif; display:flex; flex-direction:column; background:#e6f6ef; border-radius:16px; padding:20px;
       text-align:left; transition:all .25s; animation:monte .7s ease both; box-shadow:0 8px 22px rgba(15,61,110,.08)}
.kpis .kpi:nth-child(4n+1) {background:#e6f6ef}
.kpis .kpi:nth-child(4n+2) {background:#e7f0fb}
.kpis .kpi:nth-child(4n+3) {background:#fff4d6}
.kpis .kpi:nth-child(4n+4) {background:#f3ece0}
.kpi:hover {transform:translateY(-6px); box-shadow:0 16px 32px -8px rgba(15,61,110,.25)}
.kpi .ic {display:flex; align-items:center; justify-content:center; width:42px; height:42px; border-radius:50%; background:#fff; font-size:20px; box-shadow:0 4px 10px rgba(15,61,110,.10); margin-bottom:12px}
.kpi .n {color:#0f3d6e; font-size:40px; font-weight:700; line-height:1.1}
.kpi .l {color:#5b6b7e; font-size:13px; letter-spacing:1.5px; text-transform:uppercase; margin-top:6px}
.carte-photo {position:relative; border-radius:12px; overflow:hidden; border-bottom:4px solid #d4af37; box-shadow:0 10px 28px rgba(15,61,110,.25); min-height:340px; margin-bottom:12px}
.carte-photo .cbg {position:absolute; inset:0; background-size:cover; background-position:center}
.carte-photo .cvl {position:absolute; inset:0; background:linear-gradient(100deg,rgba(8,34,72,.93) 15%,rgba(10,70,92,.78) 60%,rgba(12,110,100,.50) 100%)}
.carte-photo .cin {position:relative; z-index:2; padding:26px 30px}
.carte-photo .ct {font-family:'Saira',sans-serif; color:#f3d774; font-size:22px; font-weight:700; margin-bottom:12px}
.carte-photo .cl {color:#fff; font-size:16px; line-height:1.9}
.carte-photo .cms {display:flex; gap:34px; flex-wrap:wrap; margin:4px 0 14px}
.carte-photo .cm {background:none; border:none; padding:0; min-width:120px}
.carte-photo .cml {color:#e6eefb; font-size:13px}
.carte-photo .cmv {color:#fff; font-family:'Saira',sans-serif; font-size:30px; font-weight:700; line-height:1.2}
.tbl-wrap {overflow-x:auto; background:#fff; border:1px solid #e3e8f0; border-radius:12px; box-shadow:0 4px 14px rgba(15,61,110,.06)}
.tbl {width:100%; border-collapse:collapse; font-size:14.5px}
.tbl thead th {background:#0f3d6e; color:#fff; font-family:'Saira',sans-serif; font-weight:600; letter-spacing:.4px; text-align:left; padding:13px 16px; white-space:nowrap}
.tbl td {padding:12px 16px; border-bottom:1px solid #edf1f6; color:#1b2a3a}
.tbl tbody tr:nth-child(even) td {background:#f6faf8}
.tbl tbody tr:hover td {background:#e6f6ef}
.tbl tbody tr:last-child td {border-bottom:none}
.tbl .num {text-align:right; font-variant-numeric:tabular-nums}
.tbl .vide {color:#9aa7b5}
@keyframes zoomh {from{transform:scale(1)} to{transform:scale(1.08)}}
@keyframes monte {from{opacity:0; transform:translateY(18px)} to{opacity:1; transform:none}}
@media (max-width:900px) {.kpis{grid-template-columns:repeat(2,1fr)} .hero2 .t{font-size:36px} .hero2 .in{padding:26px}}
</style>
""".replace("HEXURL", HEX)


def theme_graphiques():
    sns.set_theme(style="whitegrid", palette=PALETTE, rc={
        "figure.facecolor": "#ffffff", "axes.facecolor": "#ffffff", "savefig.facecolor": "#ffffff",
        "axes.edgecolor": "#c9d2e0", "grid.color": "#E2E8F0", "grid.linestyle": "--", "axes.spines.top": False, "axes.spines.right": False, "axes.grid.axis": "y", "legend.frameon": False, "text.color": ENCRE,
        "axes.labelcolor": ENCRE, "xtick.color": ENCRE, "ytick.color": ENCRE,
        "axes.titlecolor": BLEU, "axes.titleweight": "bold", "axes.titlesize": 14,
        "axes.labelsize": 12, "legend.facecolor": "#ffffff",
        "axes.prop_cycle": __import__("matplotlib").cycler(color=PALETTE),
    })


_cpt = [0]


def _installer_cartes_graphiques():
    """Chaque st.pyplot(...) du dashboard s'affiche dans une carte blanche, sans modifier dashboard.py."""
    if getattr(st.pyplot, "_carte", False):
        return
    original = st.pyplot

    def pyplot_carte(*args, **kwargs):
        _cpt[0] += 1
        with st.container(key=f"carte_graphique_{_cpt[0]}"):
            return original(*args, **kwargs)

    pyplot_carte._carte = True
    st.pyplot = pyplot_carte


def bandeau(badge_b64=""):
    _cpt[0] = 0
    _installer_cartes_graphiques()
    st.markdown(CSS + fond_reseau_html(), unsafe_allow_html=True)
    theme_graphiques()
    badge = f'<img class="badge" src="data:image/png;base64,{badge_b64}">' if badge_b64 else ""
    st.markdown(f"""
<div class="hero2">
<div class="bg" style="background-image:url(data:image/jpeg;base64,{_b64('slide2.jpg')})"></div><div class="vl"></div>
{badge}
<div class="in">
<span class="eb">CAMPAGNE 2026</span>
<div class="t">I.Cereal<span style="color:#d4af37">Track</span></div>
<div class="s">Plateforme de suivi agronomique · ISRA CRA Saint-Louis</div>
<div class="pills"><a class="pill" href="https://www.isra.sn" target="_blank">ISRA-CRA Saint-Louis</a>
<span class="pill">Vallée du fleuve Sénégal</span><a class="pill" href="https://www.isra.sn" target="_blank">www.isra.sn</a></div>
</div></div>""", unsafe_allow_html=True)


def cartes_chiffres(items):
    cases = "".join(
        f'<div class="kpi" style="animation-delay:{i*0.12}s"><div class="ic">{ic}</div>'
        f'<div class="n">{f"{v:,}".replace(",", " ")}</div><div class="l">{lab}</div></div>'
        for i, (v, lab, ic) in enumerate(items))
    st.markdown(f'<div class="kpis">{cases}</div>', unsafe_allow_html=True)


def carte_photo(titre, lignes, photo=None, hauteur=None):
    """Carte avec photo de fond, voile bleu marine et texte blanc."""
    import html
    photo = photo or PHOTO_CARTE
    style = f' style="min-height:{hauteur}px"' if hauteur else ""
    stats = "".join(f'<div class="cm"><div class="cml">{html.escape(str(l[0]))}</div><div class="cmv">{html.escape(str(l[1]))}</div></div>'
                    for l in lignes if isinstance(l, tuple))
    textes = "".join(f'<div class="cl">{html.escape(str(l))}</div>' for l in lignes if not isinstance(l, tuple))
    items = (f'<div class="cms">{stats}</div>' if stats else "") + textes
    st.markdown(
        f'<div class="carte-photo"{style}><div class="cbg" style="background-image:url(data:image/jpeg;base64,{_b64(photo)})"></div>'
        f'<div class="cvl"></div><div class="cin"><div class="ct">{html.escape(titre)}</div>{items}</div></div>',
        unsafe_allow_html=True)


def tableau_html(df):
    """Petit tableau sur mesure (en-tete marine, lignes fines, sans index). A reserver aux tableaux courts."""
    import html
    import numbers

    import pandas as pd

    if hasattr(df, "data") and hasattr(df, "to_html"):   # Styler pandas
        df = df.data

    def fmt(v):
        if v is None or (not isinstance(v, (list, tuple, dict)) and pd.isna(v)):
            return None
        if hasattr(v, "strftime"):
            return v.strftime("%Y-%m-%d")
        if isinstance(v, bool):
            return str(v)
        if isinstance(v, numbers.Integral):
            return f"{int(v):,}".replace(",", " ")
        if isinstance(v, numbers.Real):
            t = f"{float(v):,.2f}".rstrip("0").rstrip(".")
            return t.replace(",", " ")
        return str(v)

    colonnes = list(df.columns)
    num = [pd.api.types.is_numeric_dtype(df[c]) for c in colonnes]
    tete = "".join(f'<th class="{"num" if n else ""}">{html.escape(str(c))}</th>' for c, n in zip(colonnes, num))
    lignes = ""
    for _, ligne in df.iterrows():
        cases = ""
        for c, n in zip(colonnes, num):
            t = fmt(ligne[c])
            cls = ("num " if n else "") + ("vide" if t is None else "")
            cases += f'<td class="{cls.strip()}">{html.escape(t) if t is not None else "—"}</td>'
        lignes += f"<tr>{cases}</tr>"
    st.markdown(f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{tete}</tr></thead><tbody>{lignes}</tbody></table></div>',
                unsafe_allow_html=True)


def fond_reseau_html(opacite=0):
    # Plus d'animation de reseau : le site de reference est sobre (fond blanc).
    return ""
