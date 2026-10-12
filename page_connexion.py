import base64
from pathlib import Path

import pandas as pd
import streamlit as st

from style_interieur import fond_reseau_html
from style_champs import CSS_CHAMPS

DOSSIER = Path(__file__).parent / "images"


@st.cache_resource
def _b64(nom):
    return base64.b64encode((DOSSIER / nom).read_bytes()).decode()


@st.cache_data(ttl=600)
def _stats(_engine):
    q = lambda t: int(pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", _engine)["n"][0])
    return q("site"), q("variete"), q("mesurephichi")


CSS = """
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], footer {display:none !important}
.stApp {background:#0d2b21}
.bgfix {position:fixed; inset:-20px; z-index:0; background-size:cover; background-position:center;
        filter:blur(7px) brightness(.5) saturate(.9)}
.bgveil {position:fixed; inset:0; z-index:0; background:rgba(9,32,24,.55)}
.block-container {position:relative; z-index:1; max-width:1250px !important; padding-top:6vh !important}
.eb {display:inline-block; background:#d4af37; color:#0d2b21; font-size:15px; font-weight:800;
     letter-spacing:1.5px; padding:6px 14px; border-radius:999px}
.bienv {color:#fff; font-size:50px; line-height:1.1; font-weight:800; margin:18px 0 14px;
        text-shadow:0 2px 14px rgba(0,0,0,.65)}
.sous {color:#fff6dc; font-size:21px; line-height:1.5; max-width:520px; text-shadow:0 1px 10px rgba(0,0,0,.75)}
.stats {display:flex; gap:38px; margin-top:34px}
.num {color:#d4af37; font-size:44px; font-weight:800; line-height:1; text-shadow:0 2px 10px rgba(0,0,0,.6)}
.lab {color:#fff; font-size:14px; letter-spacing:1px; margin-top:6px}
.logo {width:64px; height:64px; border-radius:50%; border:3px solid #d4af37; background:#fff; object-fit:cover; margin-bottom:6px}
.st-key-formcard {background:rgba(9,32,24,.90); border:2px solid #d4af37; border-radius:20px;
                  padding:28px 30px; box-shadow:0 14px 44px rgba(0,0,0,.5)}
.st-key-formcard h3 {color:#d4af37; font-size:30px !important; margin:0 0 6px}
.st-key-formcard label p {font-size:1.05rem !important; font-weight:600}
.st-key-formcard input {font-size:1.05rem !important}
.st-key-formcard button[data-baseweb="tab"] p {font-size:1.1rem !important; font-weight:700}
.st-key-formcard [data-testid="stFormSubmitButton"] button {background:#d4af37; border:0; border-radius:999px;
    padding:.7rem 2rem; box-shadow:0 4px 14px rgba(0,0,0,.3)}
.st-key-formcard [data-testid="stFormSubmitButton"] button:hover {background:#b8952a}
.st-key-formcard [data-testid="stFormSubmitButton"] button * {color:#0d2b21 !important; font-weight:800; font-size:1.1rem}
@media (max-width:900px) {.bienv{font-size:34px} .sous{font-size:17px} .num{font-size:32px}}
</style>
"""


def afficher_connexion(engine, verifier_connexion, creer_utilisateur, badge_b64=""):
    st.set_page_config(page_title="I.CerealTrack - Connexion", layout="wide", page_icon="🌾")
    nb_sites, nb_var, nb_mes = _stats(engine)
    st.markdown(CSS + CSS_CHAMPS + f'<div class="bgfix" style="background-image:url(data:image/jpeg;base64,{_b64("slide2.jpg")})"></div><div class="bgveil"></div>' + fond_reseau_html(),
                unsafe_allow_html=True)

    gauche, droite = st.columns([1.15, 1], gap="large", vertical_alignment="center")

    with gauche:
        logo = f'<img class="logo" src="data:image/png;base64,{badge_b64}"><br>' if badge_b64 else ""
        st.markdown(f"""
{logo}<span class="eb">ISRA · CRA SAINT-LOUIS</span>
<div class="bienv">Bienvenue sur I.Cereal<span style="color:#d4af37">Track</span></div>
<div class="sous">Essais, climat et sol de la vallée du fleuve Sénégal, réunis au même endroit pour mieux choisir les variétés de demain.</div>
<div class="stats">
<div><div class="num">{nb_sites}</div><div class="lab">SITES SUIVIS</div></div>
<div><div class="num">{nb_var}</div><div class="lab">VARIÉTÉS</div></div>
<div><div class="num">{nb_mes:,}</div><div class="lab">MESURES COLLECTÉES</div></div>
</div>""".replace(",", " "), unsafe_allow_html=True)

    with droite:
        with st.container(key="formcard"):
            st.markdown("### Accès à I.CerealTrack")
            t_conn, t_insc = st.tabs(["Se connecter", "Créer un compte"])

            with t_conn:
                with st.form("form_connexion"):
                    email_c = st.text_input("Email", placeholder="prenom.nom@exemple.com")
                    mdp_c = st.text_input("Mot de passe", type="password")
                    valide_c = st.form_submit_button("Se connecter  →")
                if valide_c:
                    u, erreur = verifier_connexion(email_c, mdp_c)
                    if erreur:
                        st.error(erreur)
                    else:
                        st.session_state.utilisateur = dict(u)
                        st.rerun()

            with t_insc:
                with st.form("form_inscription"):
                    c1, c2 = st.columns(2)
                    i_nom = c1.text_input("Nom")
                    i_prenom = c2.text_input("Prénom")
                    c3, c4 = st.columns(2)
                    i_profession = c3.text_input("Profession")
                    i_titre = c4.text_input("Titre / fonction")
                    i_email = st.text_input("Email")
                    c5, c6 = st.columns(2)
                    i_mdp = c5.text_input("Mot de passe", type="password")
                    i_mdp2 = c6.text_input("Confirmer", type="password")
                    valide_i = st.form_submit_button("Créer mon compte  →")
                if valide_i:
                    if not (i_nom and i_prenom and i_email and i_mdp):
                        st.warning("Remplis au moins nom, prénom, email et mot de passe.")
                    elif i_mdp != i_mdp2:
                        st.error("Les deux mots de passe ne correspondent pas.")
                    else:
                        try:
                            creer_utilisateur(i_nom, i_prenom, i_profession, i_titre, i_email, i_mdp)
                            st.success("Compte créé ! Il doit maintenant être validé par un administrateur avant que tu puisses te connecter.")
                        except Exception as e:
                            st.error(f"Erreur (email déjà utilisé ?) : {e}")
    st.stop()
