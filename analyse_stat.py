import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

import graphiques_plotly as gp

VARS = {"ph": "pH", "conductivite": "Conductivité", "salinite": "Salinité", "n": "Azote (N)",
        "p": "Phosphore (P)", "k": "Potassium (K)", "temper": "Température du sol", "humidite": "Humidité du sol"}
CLIM = {"temp_moy": "Température air", "humidite_moy": "Humidité air", "rayonnement": "Rayonnement",
        "vent": "Vent", "precipitation": "Précipitations"}


def _sur(fn):
    try:
        fn()
    except Exception as e:
        st.caption(f"Analyse indisponible : {e}")


def afficher_analyse(mesures, climat=None):
    try:
        from scipy import stats
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
    except ImportError:
        st.error("Modules manquants. Dans le terminal : pip install scipy statsmodels")
        return

    m = mesures.copy()
    m["idpoint"] = m["idpoint"].astype(str).str.strip()
    m["jour"] = pd.to_datetime(m["datemesures"]).dt.normalize()
    for c in VARS:
        m[c] = pd.to_numeric(m[c], errors="coerce")
    m["variete_site"] = m["nomvariete"].astype(str) + " · " + m["nomsite"].astype(str)

    st.subheader("Comparaison de groupes (ANOVA et test de Tukey)")
    c1, c2, c3 = st.columns(3)
    var = c1.selectbox("Variable", list(VARS), format_func=VARS.get, key="st_var")
    par = c2.selectbox("Comparer par", ["variete_site", "nomvariete", "nomsite"], key="st_par",
                       format_func={"variete_site": "Variété et site", "nomvariete": "Variété", "nomsite": "Site"}.get)
    unite = c3.radio("Unité d'analyse", ["Moyenne par point (recommandé)", "Toutes les mesures"], key="st_unite")

    d = m[[par, "idpoint", var]].dropna()
    if unite.startswith("Moyenne"):
        d = d.groupby([par, "idpoint"], as_index=False)[var].mean()
    groupes = {g: x[var].values for g, x in d.groupby(par) if len(x) >= 2}
    if len(groupes) < 2:
        st.info("Il faut au moins deux groupes avec 2 valeurs chacun pour comparer.")
    else:
        def f():
            res = d[d[par].isin(groupes)].groupby(par)[var].agg(n="count", moyenne="mean", ecart_type="std",
                                                                   minimum="min", mediane="median", maximum="max")
            res["CV %"] = (res["ecart_type"] / res["moyenne"] * 100)
            st.markdown("**Statistiques descriptives**")
            st.dataframe(res.round(2), width="stretch")

            valeurs = list(groupes.values())
            F, pa = stats.f_oneway(*valeurs)
            H, pk = stats.kruskal(*valeurs)
            _, pl = stats.levene(*valeurs)
            k1, k2, k3 = st.columns(3)
            k1.metric("ANOVA : p", f"{pa:.4g}", f"F = {F:.2f}", delta_color="off")
            k2.metric("Kruskal-Wallis : p", f"{pk:.4g}", f"H = {H:.2f}", delta_color="off")
            k3.metric("Levene (variances) : p", f"{pl:.4g}", "p > 0,05 : homogènes", delta_color="off")
            if pa < 0.05:
                st.success(f"Différence significative entre les groupes au seuil de 5 % (ANOVA, p = {pa:.4g}).")
            else:
                st.info(f"Pas de différence significative au seuil de 5 % (ANOVA, p = {pa:.4g}).")
            if pl < 0.05:
                st.warning("Les variances ne sont pas homogènes : privilégiez le test de Kruskal-Wallis.")

            fig = px.box(d[d[par].isin(groupes)], x=par, y=var, color=par, points="all")
            fig.update_layout(showlegend=False, yaxis_title=VARS[var])
            gp._afficher(gp._style(fig, f"{VARS[var]} par groupe", 420))

            dd = d[d[par].isin(groupes)]
            tk = pairwise_tukeyhsd(dd[var].values, dd[par].astype(str).values)
            t = pd.DataFrame(tk.summary().data[1:], columns=tk.summary().data[0])
            t["Significatif"] = np.where(t["reject"], "Oui", "Non")
            st.markdown("**Test de Tukey : comparaisons deux à deux**")
            st.dataframe(t.drop(columns=["reject"]).rename(columns={"group1": "Groupe 1", "group2": "Groupe 2",
                         "meandiff": "Écart des moyennes", "p-adj": "p ajusté", "lower": "Borne basse", "upper": "Borne haute"}),
                         width="stretch")
            st.caption("Les mesures répétées d'un même point ne sont pas indépendantes : l'option « Moyenne par point » "
                       "évite ce problème. Les parcelles ne sont pas randomisées : ces résultats sont indicatifs.")
        _sur(f)

    st.divider()
    st.subheader("Corrélations entre variables du sol et du climat")

    def g():
        j = m.groupby(["nomsite", "jour"])[list(VARS)].mean().reset_index()
        cols = list(VARS)
        if climat is not None and len(climat):
            cl = climat.copy()
            cl["jour"] = pd.to_datetime(cl["datemesure"]).dt.normalize()
            cc = [c for c in CLIM if c in cl.columns]
            for c in cc:
                cl[c] = pd.to_numeric(cl[c], errors="coerce")
            j = j.merge(cl[["nomsite", "jour"] + cc], on=["nomsite", "jour"], how="left")
            cols += cc
        noms = {**VARS, **CLIM}
        corr = j[cols].corr().rename(index=noms, columns=noms)
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
        gp._afficher(gp._style(fig, "Matrice de corrélation (moyennes journalières par site)", 560))
        st.caption("Corrélation de Pearson : proche de 1 ou de -1, la relation est forte. Corrélation n'est pas causalité.")
    _sur(g)
