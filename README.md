# 21700 NMC (~5 Ah) Battery Cycle Data Analysis (Simulation + Degradation)

This portfolio project simulates an EV-style **21700 NMC Li-ion cell (~5 Ah, 4.2 V max)** and demonstrates:
- charge/discharge cycling (synthetic time-series)
- SOC estimation (coulomb counting + OCV correction during rest)
- temperature rise via a lumped thermal model
- degradation analysis: capacity fade, efficiency loss, resistance growth

Two conditions are compared:
1. `baseline_25C_1C`
2. `stress_35C_2C`

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
jupyter notebook
```

Open:
- `notebooks/battery_21700_nmc_simulation_and_analysis.ipynb`

## Generate PDF summary
After running the notebook (plots + CSVs must exist):
```bash
python src/make_pdf_summary.py
```

Output: `outputs/summary.pdf`
