import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ── CONFIGURATION DE LA PAGE ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatoire des Devises Algérie",
    page_icon="🇩🇿",
    layout="wide"
)

# ── GESTION DES CHEMINS (IMPORTANT POUR GITHUB/DEPLOY) ────────────────────────
# On cherche le fichier dans ../data/raw/ par rapport au dossier notebooks/
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "data", "raw", "dz_rates_combined1111.csv")

# ── CHARGEMENT DES DONNÉES ────────────────────────────────────────────────────
@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"Fichier non trouvé : {path}")
        return pd.DataFrame()
    
    df = pd.read_csv(path, sep=";")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df.sort_values("date").reset_index(drop=True)
    return df

df = load_data(csv_path)

if df.empty:
    st.stop()

# ── CONFIGURATION DES DEVISES ─────────────────────────────────────────────────
CURRENCIES = {
    "Euro (EUR)":           ("EUR_black_market_vente", "EUR_official",      "🇪🇺"),
    "Dollar US (USD)":      ("USD_black_market_vente", "USD_official",      "🇺🇸"),
    "Livre Sterling (GBP)": ("GBP_exdz_sell",          "GBP_official_sell", "🇬🇧"),
    "Dollar Canadien (CAD)": ("CAD_exdz_sell",         "CAD_official_sell", "🇨🇦"),
    "Franc Suisse (CHF)":   ("CHF_exdz_sell",          "CHF_official_sell", "🇨🇭"),
}

# ── BARRE LATÉRALE ────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🇩🇿 Observatoire")
    selected_currency = st.selectbox("Sélectionner une devise", list(CURRENCIES.keys()))
    parallel_col, official_col, flag = CURRENCIES[selected_currency]
    
    st.markdown("---")
    st.caption("Sources : Banque d'Algérie & Square (2016-2026)")

# ── PRÉPARATION ───────────────────────────────────────────────────────────────
work = df[["date"]].copy()
work["parallel"] = pd.to_numeric(df[parallel_col], errors="coerce")
work["official"] = pd.to_numeric(df[official_col], errors="coerce")
work = work.dropna(subset=["parallel"])

# ── INTERFACE ─────────────────────────────────────────────────────────────────
st.title(f"{flag} Marché Parallèle vs Officiel : {selected_currency}")

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
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

# ── GRAPHIQUE ÉPURÉ ───────────────────────────────────────────────────────────
fig = go.Figure()

# Area Marché Noir
fig.add_trace(go.Scatter(
    x=work["date"], y=work["parallel"],
    fill='tozeroy',
    name="Marché Noir",
    line=dict(color="#ff6b6b", width=3),
    fillcolor="rgba(255, 107, 107, 0.15)"
))

# Ligne Officiel
if not work["official"].dropna().empty:
    fig.add_trace(go.Scatter(
        x=work["date"], y=work["official"],
        fill='tozeroy',
        name="Officiel (Banque)",
        line=dict(color="#00d4ff", width=3),
        fillcolor="rgba(0, 212, 255, 0.15)"
    ))

fig.update_layout(
    template="plotly_dark",
    height=550,
    hovermode="x unified",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, title="Années"),
    yaxis=dict(
        showgrid=False, 
        title="DZD",
        range=[work["official"].min() * 0.85, work["parallel"].max() * 1.1]
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("📊 Historique complet des données"):
    st.dataframe(work.sort_values("date", ascending=False), use_container_width=True)
