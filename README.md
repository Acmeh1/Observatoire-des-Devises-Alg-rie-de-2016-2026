# 💱 Algeria Exchange Rate Analysis — Black Market vs Official Bank (2016–2026)

> **Tracking the gap between the official Algerian Dinar (DZD) rate and the parallel (black market) rate across 5 major currencies over a decade.**

---

## 📊 Live Dashboard

🔗 **[View on Tableau Public](https://public.tableau.com/shared/GQ4MMTMKQ?:display_count=n&:origin=viz_share_link)**
and a python interactive 
**[dashboard](https://curencies.streamlit.app/)**


---

## 🧠 Project Overview

This project analyzes the **evolution of currency exchange rates in Algeria** from 2016 to 2026, comparing:

- 🔴 **Marché Noir (Black Market)** — the parallel/informal market rate
- 🔵 **Officiel (Banque d'Algérie)** — the official central bank rate

### Currencies Covered

| Currency | Code | Black Market Peak (approx.) |
|----------|------|-----------------------------|
| Euro | EUR | ~280 DZD |
| US Dollar | USD | ~240 DZD |
| British Pound | GBP | ~300 DZD |
| Swiss Franc | CHF | ~270 DZD |
| Canadian Dollar | CAD | ~170 DZD |

---

## 📁 Data Sources

| Source | Type | URL |
|--------|------|-----|
| ExchangeDZ | Black Market rates | [exchangedz.com](https://www.exchangedz.com) |
| EuroDZ | Black Market rates | [eurodz.com](https://www.eurodz.com) |
| Bank of Algeria | Official historical rates (downloaded) | [bank-of-algeria.dz](https://www.bank-of-algeria.dz/donnees-historiques/) |

---

## 🔍 Key Findings

### Why is the black market price always higher?

1. **Strict capital controls** — Algeria heavily restricts foreign currency access through official channels, creating excess demand in informal markets.
2. **Import restrictions** — Limits on imports push individuals and businesses to source foreign currency outside the banking system.
3. **Inflation & purchasing power erosion** — Persistent inflation of the DZD widens the gap between official and real-world valuations.
4. **Hydrocarbon dependency** — Algeria's economy is oil/gas dependent; declining revenues reduce USD reserves and tighten official supply.
5. **Lack of convertibility** — The DZD is not freely convertible internationally, driving demand for the parallel market.
6. **Post-COVID economic pressure (2020–2022)** — Disrupted supply chains and reduced remittances accelerated the gap.
7. **Global USD/EUR strength (2022–2024)** — A strong dollar globally further widened the local gap.

### What are the possible solutions?

- Gradual liberalization of the exchange rate
- Developing a formal parallel window (like Egypt's managed float)
- Boosting non-hydrocarbon exports to increase FX reserves
- Easing import restrictions for SMEs
- Building trust in the banking system to bring informal savings into circulation

---

## 🛠️ Tools & Technologies

- **Python** — Data cleaning and analysis
- **Tableau** — Interactive dashboard and visualization
- **Pandas / Matplotlib** — Exploratory data analysis

---

## 📂 Repository Structure

```
├── data/
│   ├── raw/               # Raw downloaded data
│   └── processed/         # Cleaned, merged datasets per currency
├── notebooks/
│   └── dashboard.py     # EDA and preprocessing
├── dashboard/
│   └── tableau_workbook/  # Tableau workbook file
└── README.md
```

---

## 💡 Inspiration

This project was inspired by the original work of [**Abdelhak Kadouci**](https://www.linkedin.com/in/abdelhak-kadouci) who first analyzed the EUR/DZD gap. This project extends that idea to **5 currencies** with a decade of historical data and a multi-factor causal analysis.

---

## 📬 Contact

Feel free to open an issue or reach out on LinkedIn if you'd like to collaborate or discuss the findings!

---

*Data last updated: 2026 | Analysis covers 2016–2026*
