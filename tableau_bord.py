from contextlib import contextmanager

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import graphiques_plotly as gp

PH_REF = (6.0, 7.5)  # plage de reference indicative du pH, a ajuster

CSS = """
<style>
[class*="st-key-tb_"] {background:#ffffff; border-radius:14px; padding:16px 18px 10px; box-shadow:0 2px 14px rgba(0,0,0,.10)}
.tb-t {text-align:center; font-weight:700; font-size:1.05rem; color:#1f2d2a; width:70%; margin:0 auto 10px; padding-bottom:6px; border-bottom:1px solid rgba(0,0,0,.14)}
.tb-kpi {text-align:center; padding:26px 6px 18px}
.tb-kpi .n {font-size:48px; font-weight:800; color:#c9971c; line-height:1.1}
.tb-kpi .s {color:#5a6b66; font-size:1rem; margin-top:10px; line-height:1.6}
</style>
"""


@contextmanager
def carte(cle, titre):
    with st.container(key="tb_" + cle):
        st.markdown(f'<div class="tb-t">{titre}</div>', unsafe_allow_html=True)
        yield


def _show(fig, h=300, titre=None):
    gp._afficher(gp._style(fig, titre, h))


def _sur(fn):
    try:
        fn()
    except Exception as e:
        st.caption(f"Graphique indisponible : {e}")


def _score(x):
    x = str(x).lower()
    return 20 if "sensible" in x else 60 if "moyen" in x else 100 if "resist" in x else 0


def afficher_tableau_bord(mesures, sites, varietes, synthese, climat, engine):
    st.markdown(CSS, unsafe_allow_html=True)
    m = mesures.copy()
    m["jour"] = pd.to_datetime(m["datemesures"])
    m["idpoint"] = m["idpoint"].astype(str).str.strip()
    for c in ["ph", "salinite", "conductivite"]:
        m[c] = pd.to_numeric(m[c], errors="coerce")
    nb_jours = max(m["jour"].dt.date.nunique(), 1)

    # ---- Ligne 1
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1, carte("jour", "Mesures par jour"):
        def f():
            d = m.groupby(m["jour"].dt.date).size().reset_index()
            d.columns = ["Jour", "Mesures"]
            fig = px.bar(d, x="Jour", y="Mesures")
            fig.update_traces(marker_color=gp.OR)
            fig.update_layout(bargap=0.25)
            _show(fig, 300)
        _sur(f)
    with c2, carte("kpi", "Mesures du sol"):
        n = f"{len(m):,}".replace(",", " ")
        st.markdown(f'<div class="tb-kpi"><div class="n">{n}</div><div class="s">environ {len(m) // nb_jours} par jour<br>'
                    f'{m["idpoint"].nunique()} points de prélèvement<br>{m["nomvariete"].nunique()} variétés suivies</div></div>',
                    unsafe_allow_html=True)
    with c3, carte("site", "Répartition par site"):
        def f():
            d = m["nomsite"].value_counts().reset_index()
            d.columns = ["Site", "Mesures"]
            fig = px.pie(d, names="Site", values="Mesures", hole=0.6)
            fig.update_traces(textinfo="percent")
            _show(fig, 300)
        _sur(f)

    # ---- Ligne 2
    c1, c2, c3 = st.columns(3)
    with c1, carte("variete", "Répartition par variété"):
        def f():
            d = m["nomvariete"].value_counts().reset_index()
            d.columns = ["Variété", "Mesures"]
            fig = px.pie(d, names="Variété", values="Mesures", hole=0.6)
            fig.update_traces(textinfo="percent")
            _show(fig, 320)
        _sur(f)
    with c2, carte("sal", "10 points les plus salins"):
        def f():
            d = m.groupby("idpoint")["salinite"].mean().dropna().sort_values().tail(10).reset_index()
            fig = px.bar(d, x="salinite", y="idpoint", orientation="h")
            fig.update_traces(marker_color=gp.PAL[3])
            fig.update_layout(yaxis_title="", xaxis_title="Salinité moyenne")
            _show(fig, 320)
        _sur(f)
    with c3, carte("ph", "Distribution du pH"):
        def f():
            fig = px.histogram(m.dropna(subset=["ph"]), x="ph", nbins=30)
            fig.update_traces(marker_color=gp.PAL[0])
            fig.update_layout(xaxis_title="pH", yaxis_title="Mesures", bargap=0.05)
            _show(fig, 320)
        _sur(f)

    # ---- Ligne 3 : carte + jauges
    c1, c2 = st.columns([2, 1])
    with c1, carte("carte", "Carte des points de prélèvement"):
        def f():
            choix = st.radio("Colorer selon", ["pH", "Salinité", "Conductivité"], horizontal=True, key="tb_carte_var")
            col = {"pH": "ph", "Salinité": "salinite", "Conductivité": "conductivite"}[choix]
            pts = pd.read_sql("SELECT idpoint, latitude, longitude FROM pointechanti WHERE latitude IS NOT NULL", engine)
            pts["idpoint"] = pts["idpoint"].astype(str).str.strip()
            moy = m.groupby("idpoint")[["ph", "salinite", "conductivite"]].mean().reset_index()
            d = pts.merge(moy, on="idpoint").dropna(subset=[col])
            if d.empty:
                st.info("Aucun point géolocalisé avec des mesures.")
                return
            kw = dict(lat="latitude", lon="longitude", color=col, hover_name="idpoint", color_continuous_scale="Viridis", zoom=11)
            try:
                fig = px.scatter_map(d, map_style="open-street-map", **kw)
            except (AttributeError, TypeError):
                fig = px.scatter_mapbox(d, mapbox_style="open-street-map", **kw)
            fig.update_traces(marker=dict(size=13))
            fig.update_layout(coloraxis_colorbar=dict(title=choix))
            _show(fig, 420)
        _sur(f)
    with c2, carte("jauge", "Valeurs moyennes"):
        def f():
            ph = m["ph"].mean()
            sal = m["salinite"].mean()
            g1 = go.Figure(go.Indicator(mode="gauge+number", value=round(ph, 2), title={"text": "pH moyen"},
                gauge=dict(axis=dict(range=[5, 10]), bar=dict(color=gp.OR),
                           steps=[dict(range=list(PH_REF), color="rgba(30,122,79,.25)")])))
            _show(g1, 200)
            g2 = go.Figure(go.Indicator(mode="gauge+number", value=round(sal, 1), title={"text": "Salinité moyenne"},
                gauge=dict(axis=dict(range=[0, max(300, sal * 1.5)]), bar=dict(color=gp.PAL[3]))))
            _show(g2, 200)
            st.caption(f"Zone verte du pH : plage de référence indicative {PH_REF[0]} – {PH_REF[1]}.")
        _sur(f)

    # ---- Ligne 4 : radar des variétés
    with carte("radar", "Comparaison des variétés"):
        def f():
            v = varietes.copy()
            labs = []
            for lab, col in {"Rendement potentiel": "rendement_potentiel_isra", "Rendement moyen": "rendement_moyen_isra",
                             "Protéines": "proteine_pct"}.items():
                s = pd.to_numeric(v[col], errors="coerce")
                v[lab] = (s / s.max() * 100).fillna(0) if s.max() else 0
                labs.append(lab)
            for lab, col in {"Résist. chaleur": "resistance_chaleur", "Résist. salinité": "resistance_salinite",
                             "Résist. verse": "resistance_verse"}.items():
                v[lab] = v[col].apply(_score)
                labs.append(lab)
            noms = v["nomvariete"].tolist()
            choix = st.multiselect("Variétés à comparer", noms, default=noms[:2], key="tb_radar_sel")
            fig = go.Figure()
            for nom in choix:
                r = v.loc[v["nomvariete"] == nom, labs].iloc[0].tolist()
                fig.add_trace(go.Scatterpolar(r=r + r[:1], theta=labs + labs[:1], fill="toself", name=nom, opacity=0.65))
            fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100], visible=True)))
            _show(fig, 440)
            st.caption("Les valeurs manquantes de la fiche variété comptent pour 0 : complétez la fiche pour une comparaison juste.")
        _sur(f)
