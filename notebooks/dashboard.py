import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── CONFIGURATION DE LA PAGE ──────────────────────────────────────────────────
st.set_page_config(
    page_title="DZD Dashboard Épuré",
    page_icon="🇩🇿",
    layout="wide"
)

# ── CHARGEMENT DES DONNÉES ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Remplace par ton chemin si nécessaire
    df = pd.read_csv(r"C:\Users\max\Downloads\dz_rates_combined1111.csv", sep=";")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df.sort_values("date").reset_index(drop=True)
    return df

df = load_data()

# ── CONFIGURATION DES DEVISES ─────────────────────────────────────────────────
CURRENCIES = {
    "Euro (EUR)":          ("EUR_black_market_vente", "EUR_official",      "🇪🇺"),
    "Dollar US (USD)":     ("USD_black_market_vente", "USD_official",      "🇺🇸"),
    "Livre Sterling (GBP)":("GBP_exdz_sell",          "GBP_official_sell", "🇬🇧"),
    "Dollar Canadien (CAD)":("CAD_exdz_sell",         "CAD_official_sell", "🇨🇦"),
    "Franc Suisse (CHF)":  ("CHF_exdz_sell",          "CHF_official_sell", "🇨🇭"),
}

# ── BARRE LATÉRALE (FILTRES) ──────────────────────────────────────────────────
with st.sidebar:
    st.title("🇩🇿 Filtres")
    selected_currency = st.selectbox("Sélectionner une devise", list(CURRENCIES.keys()))
    parallel_col, official_col, flag = CURRENCIES[selected_currency]
    
    st.markdown("---")
    st.caption("Data source : Banque d'Algérie & euro-dz.com & exchangedz.com ")

# ── PRÉPARATION DES DONNÉES FILTRÉES ──────────────────────────────────────────
work = df[["date"]].copy()
work["parallel"] = pd.to_numeric(df[parallel_col], errors="coerce")
work["official"] = pd.to_numeric(df[official_col], errors="coerce")
work = work.dropna(subset=["parallel"])

# ── INTERFACE PRINCIPALE ──────────────────────────────────────────────────────
st.title(f"{flag} Analyse des Taux : {selected_currency}")

# ── KPI CARDS (CHIFFRES CLÉS) ─────────────────────────────────────────────────
latest = work.iloc[-1]
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📈 Marché Noir (Square)", f"{latest['parallel']:.1f} DZD")

with col2:
    off_val = latest['official']
    st.metric("🏦 Banque (Officiel)", f"{off_val:.2f} DZD" if pd.notna(off_val) else "N/A")

with col3:
    if pd.notna(off_val):
        gap = latest['parallel'] - off_val
        gap_pct = (gap / off_val) * 100
        st.metric("📊 Écart (Gap)", f"{gap:.1f} DZD", delta=f"{gap_pct:.1f}%")

st.markdown("---")

# ── GRAPHIQUE : PARALLEL VS OFFICIAL (DESIGN ÉPURÉ) ───────────────────────────
st.subheader("📈 Évolution des Taux dans le Temps")

fig = go.Figure()

# Zone de remplissage (Area) pour le Marché Noir
fig.add_trace(go.Scatter(
    x=work["date"], y=work["parallel"],
    fill='tozeroy',
    name="Marché Noir",
    line=dict(color="#ff6b6b", width=3),
    fillcolor="rgba(255, 107, 107, 0.2)" # Dégradé léger
))

# Ligne pour le Marché Officiel
if not work["official"].dropna().empty:
    fig.add_trace(go.Scatter(
        x=work["date"], y=work["official"],
        fill='tozeroy',
        name="Officiel (Banque)",
        line=dict(color="#00d4ff", width=3),
        fillcolor="rgba(0, 212, 255, 0.2)" # Dégradé léger
    ))

# RÉGLAGES DU DESIGN (Suppression des lignes et carrés)
fig.update_layout(
    template="plotly_dark",
    height=500,
    hovermode="x unified",
    paper_bgcolor="rgba(0,0,0,0)", # Fond transparent
    plot_bgcolor="rgba(0,0,0,0)",  # Fond du graphique transparent
    xaxis=dict(
        showgrid=False,       # Supprime les lignes verticales
        zeroline=False, 
        title="Date"
    ),
    yaxis=dict(
        showgrid=False,       # Supprime les lignes horizontales (les carrés)
        zeroline=True,
        zerolinecolor="gray",
        title="DZD",
        range=[work["official"].min() * 0.9, work["parallel"].max() * 1.1] # Auto-zoom (pas de vide en bas)
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=20, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# ── TABLEAU DE DONNÉES ────────────────────────────────────────────────────────
with st.expander("Voir les données brutes"):
    st.dataframe(work.sort_values("date", ascending=False), use_container_width=True)