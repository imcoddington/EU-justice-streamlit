# EU Justice Dashboard

This repository contains modules for the **EU Copilot App**, a Streamlit-based data dashboard designed to explore key issues in **Access to Justice** across EU countries. Developed by Isabella Coddington, the dashboard integrates survey data, interactive visualizations, and secure cloud-based data retrieval to examine dimensions of legal need, resolution, and the justice gap.

## 📂 Modules

### `1_A2J_Dashboard.py`
**Title:** Access to Justice Dashboard  
This module powers the **QRQ (Query-Resolve-Quality)** Dashboard tab, enabling users to explore:
- Patterns in justice-related needs
- Rates of problem resolution
- Measures of fairness, timeliness, and process quality

### `2_Justice_Gap.py`
**Title:** Dissecting the Justice Gap  
This module visualizes and analyzes the **gap between legal problems experienced and those fully resolved**, featuring:
- Justice Gap indicators across regions
- Problem type breakdowns
- Time-to-resolution plots

## 🔐 Authentication
Password protection and Dropbox token authentication are implemented via custom `tools/passcheck.py`. Sensitive credentials are accessed through Streamlit’s secrets manager.
