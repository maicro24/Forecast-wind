# 🌪️ Strong Wind Early Warning System (Algeria)

This project is an end-to-end **Python data pipeline** that analyzes **hourly weather forecasts** and automatically detects **dangerous wind gust hours**.

Instead of answering:
> "Which day will be windy?"

This project answers:
> **"Which hour exactly is dangerous?"**

The project focuses on **Algerian cities (Oran & Algiers)**.

---

## 🚨 What does this project do?

- Downloads hourly wind forecast data from **Open-Meteo (ECMWF/GFS models)**
- Cleans and structures the data
- Analyzes:
  - Mean wind speed
  - Wind gusts
- Detects **dangerous hours** where:
gust ≥ 80 km/h

- Outputs:
- Excel reports
- Interactive charts (Plotly)

