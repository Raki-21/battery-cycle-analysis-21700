from pathlib import Path
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def main():
    outdir = Path("outputs")
    outdir.mkdir(exist_ok=True)
    pdf_path = outdir / "summary.pdf"

    # Load KPIs
    kpi_base = outdir / "cycle_kpis_baseline_25C_1C.csv"
    kpi_stress = outdir / "cycle_kpis_stress_35C_2C.csv"
    base = pd.read_csv(kpi_base) if kpi_base.exists() else None
    stress = pd.read_csv(kpi_stress) if kpi_stress.exists() else None

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    w, h = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.8*inch, h-0.9*inch, "21700 NMC (~5 Ah) — Cycle Degradation Summary")
    c.setFont("Helvetica", 10)
    c.drawString(0.8*inch, h-1.15*inch, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y = h-1.55*inch
    c.setFont("Helvetica", 11)
    bullets = [
        "Two-condition comparison: baseline (25C, 1C) vs stress (35C, 2C).",
        "Synthetic but plausible signals: V(t), SOC, temperature, per-cycle KPIs.",
        "KPIs: discharge capacity, coulombic efficiency, energy efficiency, resistance growth (model).",
    ]
    for b in bullets:
        c.drawString(0.9*inch, y, u"\u2022 " + b)
        y -= 0.22*inch

    def add_block(title, df, y):
        if df is None or len(df) < 2:
            return y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.8*inch, y, title)
        y -= 0.25*inch
        c.setFont("Helvetica", 11)

        cap0 = float(df.loc[0, "Q_dis_Ah"])
        cap_end = float(df.loc[len(df)-1, "Q_dis_Ah"])
        ret = cap_end / cap0
        ce_end = float(df.loc[len(df)-1, "coul_eff"])
        ee_end = float(df.loc[len(df)-1, "energy_eff"])
        tmax = float(df["Tmax_C"].max())

        lines = [
            f"Cycles: {len(df)}",
            f"Capacity retention: {ret*100:.1f}%",
            f"Final coulombic efficiency: {ce_end*100:.2f}%",
            f"Final energy efficiency: {ee_end*100:.2f}%",
            f"Peak temperature: {tmax:.1f} C",
        ]
        for ln in lines:
            c.drawString(0.9*inch, y, ln)
            y -= 0.20*inch
        return y - 0.10*inch

    y = add_block("Baseline (25C, 1C)", base, y)
    y = add_block("Stress (35C, 2C)", stress, y)

    # Page 1 charts
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8*inch, 5.1*inch, "Comparison Charts")
    chart_files = [
        "compare_voltage_cycle60.png",
        "compare_temperature_cycle60.png",
        "compare_capacity_fade.png",
        "compare_capacity_retention.png",
    ]
    charts = [outdir/f for f in chart_files if (outdir/f).exists()]
    placements = [
        (0.8*inch, 3.1*inch, 3.9*inch, 2.3*inch),
        (4.3*inch, 3.1*inch, 3.9*inch, 2.3*inch),
        (0.8*inch, 0.6*inch, 3.9*inch, 2.3*inch),
        (4.3*inch, 0.6*inch, 3.9*inch, 2.3*inch),
    ]
    for i, p in enumerate(charts[:4]):
        x,y0,w0,h0 = placements[i]
        c.drawImage(str(p), x, y0, width=w0, height=h0, preserveAspectRatio=True, anchor='sw')

    c.showPage()

    # Page 2 charts
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.8*inch, h-0.9*inch, "Efficiency + Resistance")
    chart_files2 = [
        "compare_energy_efficiency.png",
        "compare_coulombic_efficiency.png",
        "compare_resistance_growth.png",
        "compare_soc_est_cycle60.png",
    ]
    charts2 = [outdir/f for f in chart_files2 if (outdir/f).exists()]
    placements2 = [
        (0.8*inch, 3.1*inch, 3.9*inch, 2.3*inch),
        (4.3*inch, 3.1*inch, 3.9*inch, 2.3*inch),
        (0.8*inch, 0.6*inch, 3.9*inch, 2.3*inch),
        (4.3*inch, 0.6*inch, 3.9*inch, 2.3*inch),
    ]
    for i, p in enumerate(charts2[:4]):
        x,y0,w0,h0 = placements2[i]
        c.drawImage(str(p), x, y0, width=w0, height=h0, preserveAspectRatio=True, anchor='sw')

    c.save()
    print("Wrote", pdf_path)

if __name__ == "__main__":
    main()
