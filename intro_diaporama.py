import base64
import html
from pathlib import Path

import streamlit as st

DOSSIER = Path(__file__).parent / "images"
SEC = 6  # secondes par image

SLIDES = [
    ("slide1.jpg", "RIZ · LES VARIÉTÉS DE DEMAIN", "Le riz de demain naît dans la vallée du fleuve Sénégal",
     "51 nouvelles lignes de riz passent l'épreuve du terrain. Laquelle deviendra la championne de la vallée ?"),
    ("slide2.jpg", "BLÉ DUR", "Le blé dur prend racine, épi après épi",
     "Sol, climat, rendement : on suit chaque parcelle de près pour dénicher les variétés les plus performantes."),
    ("slide3.jpg", "IRRIGATION", "Chaque goutte d'eau compte",
     "Bien gérée, l'eau rend possibles les cultures de contre-saison. La recherche mesure, compare et affine."),
    ("slide4.jpg", "SEMENCES CERTIFIÉES", "Des graines de confiance pour les producteurs",
     "Contre-saison froide 2025 : des semences d'arachide certifiées, du champ jusqu'à l'agriculteur."),
    ("slide5.jpg", "SUR LE TERRAIN", "La recherche, les pieds dans les parcelles",
     "Chercheurs, techniciens et partenaires observent ensemble les essais, ligne après ligne."),
    ("slide6.jpg", "OBSERVER · MESURER · DÉCIDER", "Chaque épi raconte une histoire",
     "Les observations de terrain alimentent la base de données pour mieux choisir les variétés."),
    ("slide7.jpg", "ISRA · CRA SAINT-LOUIS", "Pour celles et ceux qui nous nourrissent",
     "Derrière chaque donnée, des producteurs et des productrices. Ensemble, faisons pousser de meilleures récoltes !"),
]


@st.cache_resource
def _b64(nom):
    return base64.b64encode((DOSSIER / nom).read_bytes()).decode()


def afficher_intro(badge_b64=""):
    st.set_page_config(page_title="I.CerealTrack", layout="wide", page_icon="🌾")
    n = len(SLIDES)
    dur = SEC * n
    s = 100 / n
    fonds, textes, dots = [], [], []
    for i, (img, eyebrow, titre, texte) in enumerate(SLIDES):
        d = i * SEC
        fonds.append(f'<div class="sl" style="background-image:url(data:image/jpeg;base64,{_b64(img)});animation-delay:{d}s"></div>')
        textes.append(
            f'<div class="tx" style="animation-delay:{d}s"><div class="eb">{html.escape(eyebrow)}</div>'
            f'<h1>{html.escape(titre)}</h1><p>{html.escape(texte)}</p></div>')
        dots.append(f'<div class="dot" style="animation-delay:{d}s"></div>')

    css = f"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], footer {{display:none !important}}
.stApp {{background:radial-gradient(circle at 15% 0%,#1e6b4f 0%,#0d2b21 70%)}}
.block-container {{padding:0 !important; max-width:100% !important}}
.hero {{position:fixed; inset:0; overflow:hidden; z-index:0}}
.bg {{position:absolute; inset:-20px; background-size:cover; background-position:center; filter:blur(7px) brightness(.5) saturate(.9)}}
.frame {{position:absolute; z-index:2; right:5vw; top:50%; transform:translateY(-50%); width:66vw; height:min(64vh,580px); border:4px solid #d4af37; border-radius:18px; overflow:hidden; box-shadow:0 14px 44px rgba(0,0,0,.45)}}
.frame::before {{content:''; position:absolute; inset:0; z-index:1; background:linear-gradient(90deg,rgba(9,32,24,.80) 0%,rgba(9,32,24,.45) 45%,rgba(9,32,24,0) 75%)}}
.sl {{position:absolute; inset:0; background-size:cover; background-position:center; opacity:0; animation:fond {dur}s infinite}}
.veil {{position:absolute; inset:0; background:rgba(9,32,24,.55)}}
.bar {{position:absolute; top:0; left:0; right:0; z-index:3; display:flex; align-items:center; gap:14px; padding:18px 5vw; color:#fff; font-weight:600; letter-spacing:.5px; font-size:18px}}
.bar img {{width:54px; height:54px; border-radius:50%; border:3px solid #d4af37; background:#fff; object-fit:cover}}
.bar span.r {{margin-left:auto; font-weight:500; opacity:.9}}
:root {{--H:min(560px, calc(100vh - 190px))}}
.card {{position:absolute; z-index:3; left:5vw; top:calc(50vh + 20px - var(--H)/2); width:min(560px,90vw); height:var(--H); background:transparent}}
.tx {{position:absolute; inset:0; padding:clamp(18px,3.5vh,34px) 38px 100px; opacity:0; animation:texte {dur}s infinite}}
.tx .eb {{display:inline-block; background:#d4af37; color:#0d2b21; font-size:15px; font-weight:800; letter-spacing:1.5px; padding:6px 14px; border-radius:999px}}
.tx h1 {{color:#fff; text-shadow:0 2px 14px rgba(0,0,0,.65); font-size:clamp(26px,5.6vh,44px); line-height:1.15; margin:clamp(8px,2vh,16px) 0 clamp(8px,1.6vh,14px); padding:0; font-weight:800}}
.tx p {{color:#fff6dc; text-shadow:0 1px 10px rgba(0,0,0,.75); font-size:clamp(15px,2.8vh,21px); line-height:1.5; margin:0}}
.dots {{position:absolute; z-index:3; bottom:30px; left:0; right:0; display:flex; justify-content:center; gap:10px}}
.dot {{width:34px; height:5px; border-radius:3px; background:rgba(255,255,255,.35); animation:pt {dur}s infinite}}
.st-key-entrer {{position:fixed; z-index:10; left:calc(5vw + 38px); top:calc(50vh + 20px + var(--H)/2 - 92px); width:auto !important}}
.st-key-entrer button {{background:#d4af37; border:0; border-radius:999px; padding:.8rem 2rem; box-shadow:0 4px 14px rgba(0,0,0,.25)}}
.st-key-entrer button:hover {{background:#b8952a}}
.st-key-entrer button * {{color:#0d2b21 !important; font-weight:700; font-size:1.2rem}}
@keyframes fond {{0%{{opacity:0;transform:scale(1)}} {s*.18:.2f}%{{opacity:1}} {s:.2f}%{{opacity:1}} {s*1.18:.2f}%{{opacity:0;transform:scale(1.12)}} 100%{{opacity:0;transform:scale(1.12)}}}}
@keyframes texte {{0%{{opacity:0;transform:translateY(14px)}} {s*.2:.2f}%{{opacity:1;transform:none}} {s*.95:.2f}%{{opacity:1}} {s*1.1:.2f}%{{opacity:0}} 100%{{opacity:0}}}}
@keyframes pt {{0%,{s:.2f}%{{background:#d4af37;width:54px}} {s*1.1:.2f}%,100%{{background:rgba(255,255,255,.35);width:34px}}}}
@media (max-width:900px) {{.frame{{left:5vw;right:5vw;width:auto;top:16vh;transform:none;height:34vh}} .card{{top:auto;bottom:70px;left:5vw;height:430px}} .st-key-entrer{{top:auto;bottom:86px}}}}
@media (max-width:640px) {{.tx h1{{font-size:28px}} .tx p{{font-size:16px}}}}
</style>
"""
    badge = f'<img src="data:image/png;base64,{badge_b64}">' if badge_b64 else ""
    st.markdown(css + f"""
<div class="hero"><div class="bg" style="background-image:url(data:image/jpeg;base64,{_b64('slide2.jpg')})"></div><div class="veil"></div><div class="frame">{''.join(fonds)}</div>
<div class="bar">{badge}<span style="font-weight:800; font-size:24px">I.Cereal<span style="color:#d4af37">Track</span></span><span style="opacity:.85; font-weight:500; font-size:16px">· ISRA CRA Saint-Louis</span><span class="r">Plateforme de suivi agronomique · Campagne 2026</span></div>
<div class="card">{''.join(textes)}</div>
<div class="dots">{''.join(dots)}</div></div>
""", unsafe_allow_html=True)

    if st.button("Entrer dans la plateforme  →", key="entrer"):
        st.session_state.intro_vue = True
        st.rerun()
    st.stop()
