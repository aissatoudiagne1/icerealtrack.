import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

OR, VERT = "#d4af37", "#4fae7b"
THEME_CLAIR = True  # False si l'interieur de la plateforme est sombre

if THEME_CLAIR:
    PAL = ["#1e7a4f", "#c9971c", "#2f7fb5", "#d9772b", "#6b7c85", "#8e6bb0"]
    TXT, GRILLE, TITRE, TEMPLATE = "#1f2d2a", "rgba(0,0,0,0.09)", "#1b5e3a", "plotly_white"
    HOVER_BG, PLOT_BG, REF = "#ffffff", "rgba(0,0,0,0.02)", "rgba(120,144,156,0.5)"
else:
    PAL = ["#d4af37", "#4fae7b", "#5fa8d3", "#e0975a", "#a3b18a", "#cfd8dc"]
    TXT, GRILLE, TITRE, TEMPLATE = "#f3f0e6", "rgba(255,255,255,0.08)", OR, "plotly_dark"
    HOVER_BG, PLOT_BG, REF = "#0d2b21", "rgba(255,255,255,0.04)", "rgba(207,216,220,0.55)"


def _style(fig, titre=None, h=380):
    fig.update_layout(
        template=TEMPLATE, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PLOT_BG,
        font=dict(color=TXT, size=14), height=h, colorway=PAL,
        title=dict(text=titre, x=0, font=dict(size=18, color=TITRE)) if titre else None,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", y=1.02, yanchor="bottom", x=1, xanchor="right", bgcolor="rgba(0,0,0,0)", title_text=""),
        hoverlabel=dict(bgcolor=HOVER_BG, bordercolor=OR, font_size=14, font_color=TXT),
    )
    fig.update_xaxes(gridcolor=GRILLE, zeroline=False, title_text="")
    fig.update_yaxes(gridcolor=GRILLE, zeroline=False)
    try:
        fig.update_traces(marker_cornerradius=6, selector=dict(type="bar"))
    except Exception:
        pass
    return fig


def _afficher(fig):
    cfg = {"displaylogo": False}
    try:
        st.plotly_chart(fig, width="stretch", config=cfg)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, config=cfg)


def _vide(df):
    if df is None or len(df) == 0:
        st.info("Aucune donnée à afficher avec les filtres actuels.")
        return True
    return False


def barres_sites(sites, mesures):
    noms = sites["nomsite"].tolist()
    d = pd.DataFrame({"Site": noms, "Mesures": [int((mesures["nomsite"] == n).sum()) for n in noms]})
    fig = px.bar(d, x="Site", y="Mesures", color="Site", text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(showlegend=False, bargap=0.55)
    _afficher(_style(fig, None, 320))


def comparaison_varietes(varietes, choisie):
    d = varietes.copy()
    couleurs = [OR if n == choisie else "rgba(79,174,123,0.55)" for n in d["nomvariete"]]
    fig = go.Figure(go.Bar(x=d["nomvariete"], y=d["rendement_potentiel_isra"], marker_color=couleurs,
                           hovertemplate="%{x}<br>%{y} T/ha<extra></extra>"))
    fig.update_layout(bargap=0.45, yaxis_title="Rendement potentiel (T/ha)")
    _afficher(_style(fig, "Position de cette variété par rapport aux autres", 380))


def rendement_vs_reference(comp):
    d = comp.copy()
    d["Essai"] = d["nomvariete"] + " (" + d["nomsite"] + ")"
    fig = go.Figure()
    fig.add_bar(x=d["Essai"], y=d["rendement_moyen_isra"], name="Référence ISRA", marker_color=REF)
    fig.add_bar(x=d["Essai"], y=d["rendement_moyen"], name="Mesuré dans l'essai", marker_color=OR)
    fig.update_layout(barmode="group", bargap=0.4, yaxis_title="T/ha")
    _afficher(_style(fig, None, 380))


def courbes(df, xcol, ycol, titre):
    if _vide(df):
        return
    d = df.sort_values(xcol)
    fig = px.line(d, x=xcol, y=ycol, color="nomsite")
    fig.update_traces(line=dict(width=2.5), hovertemplate="%{x}<br>%{y:.2f}<extra>%{fullData.name}</extra>")
    fig.update_layout(hovermode="x unified", yaxis_title="")
    fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.08))
    _afficher(_style(fig, titre, 430))


def boite(df, ycol, titre, par="nomsite"):
    if _vide(df):
        return
    fig = px.box(df, x=par, y=ycol, color=par, points="outliers")
    fig.update_traces(line=dict(width=2))
    fig.update_layout(showlegend=False, yaxis_title="")
    _afficher(_style(fig, titre, 400))


def mensuel(df, ycol, titre, par="nomsite"):
    if _vide(df):
        return
    d = df.sort_values("mois")
    fig = px.line(d, x="mois", y=ycol, color=par, markers=True)
    fig.update_traces(line=dict(width=3), marker=dict(size=9), hovertemplate="%{x}<br>%{y:.2f}<extra>%{fullData.name}</extra>")
    fig.update_layout(hovermode="x unified", yaxis_title="")
    _afficher(_style(fig, titre, 400))
