"""Create a concise project status report PDF."""
from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "reports" / "generated" / "metrics.json"
OUTPUT = ROOT / "outputs" / "Kaushik_Project_Update_Report.pdf"
RESULTS = ROOT / "reports" / "generated"
NAVY = colors.HexColor("#123B52")
TEAL = colors.HexColor("#147D92")
PALE = colors.HexColor("#EEF4F6")
INK = colors.HexColor("#202A30")
MUTED = colors.HexColor("#52616B")


def styleset():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, alignment=1, textColor=NAVY, spaceAfter=7))
    styles.add(ParagraphStyle(name="Subtitle", parent=styles["Heading2"], fontName="Helvetica", fontSize=12, leading=15, alignment=1, textColor=INK, spaceAfter=7))
    styles.add(ParagraphStyle(name="SectionX", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=NAVY, spaceBefore=7, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle(name="SubsectionX", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=9.8, leading=12, textColor=TEAL, spaceBefore=5, spaceAfter=2, keepWithNext=True))
    styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.7, leading=11.5, textColor=INK, spaceAfter=4))
    styles.add(ParagraphStyle(name="SmallX", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.3, leading=9, textColor=MUTED, spaceAfter=3))
    styles.add(ParagraphStyle(name="CellX", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.3, leading=9, textColor=INK))
    styles.add(ParagraphStyle(name="CellHeadX", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.3, leading=8.5, textColor=colors.white))
    styles.add(ParagraphStyle(name="Status", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=17, alignment=1, textColor=TEAL, spaceAfter=6))
    return styles


def p(text, style):
    return Paragraph(text, style)


def make_table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#C8D5DA")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CAD6DC"))
    canvas.line(.62*inch, .43*inch, 7.88*inch, .43*inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(.62*inch, .27*inch, "Aircraft Turbofan Predictive Maintenance | Project status update")
    canvas.drawRightString(7.88*inch, .27*inch, f"Page {document.page}")
    canvas.restoreState()


def main():
    m = json.loads(METRICS.read_text())
    s = styleset()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, rightMargin=.62*inch, leftMargin=.62*inch,
        topMargin=.48*inch, bottomMargin=.58*inch,
        title="Project Update Report - Predictive Maintenance of Aircraft Turbofan Engines",
        author="Kaushik Kakad",
    )
    story = []

    # Page 1: project scope and current progress.
    story += [
        p("PROJECT UPDATE REPORT", s["Cover"]),
        p("Predictive Maintenance of Aircraft Turbofan Engines Using Machine Learning", s["Subtitle"]),
        p("Prepared by Kaushik Kakad", s["BodyX"]),
        p("ESTIMATED PROJECT COMPLETION: 40%", s["Status"]),
        p("Project overview", s["SectionX"]),
        p("This project investigates whether turbofan sensor measurements can estimate remaining useful life (RUL) and support condition-based maintenance planning. The proposal established the problem, objective, research direction, and initial references. The current project includes an FD001 data pipeline, engineered sensor features, two baseline models, and first validation and test results. The work remains in progress; further analysis, robust evaluation, model improvement, and final refinement are still needed.", s["BodyX"]),
        p("Objective and working questions", s["SectionX"]),
        p("<b>Objective:</b> Build and evaluate machine-learning approaches that estimate cycles remaining before simulated turbofan failure, then examine how prediction errors affect maintenance planning. Working questions: (1) Can operating settings and sensor histories predict RUL? (2) How does a tree ensemble compare with a regularized linear baseline? (3) How well do validation results carry over to official test engines? (4) What additional checks are needed before the estimates could support maintenance decisions?", s["BodyX"]),
        p("Progress status", s["SectionX"]),
    ]
    status = [
        [p("Component", s["CellHeadX"]), p("Status", s["CellHeadX"]), p("What is done or remains", s["CellHeadX"])],
        [p("Proposal and project framing", s["CellX"]), p("Complete", s["CellX"]), p("Problem, objective, working questions, and starting references are established.", s["CellX"])],
        [p("Data and features", s["CellX"]), p("Implemented for FD001", s["CellX"]), p("Loads C-MAPSS, creates RUL labels, and calculates per-engine rolling sensor summaries.", s["CellX"])],
        [p("Baseline models", s["CellX"]), p("Initial comparison complete", s["CellX"]), p("Ridge regression and Random Forest are trained and compared.", s["CellX"])],
        [p("Analysis and extensions", s["CellX"]), p("In progress", s["CellX"]), p("Investigate the test error gap, strengthen validation, and compare additional data or models.", s["CellX"])],
        [p("Final refinement", s["CellX"]), p("Remaining", s["CellX"]), p("Complete error analysis, conclusions, and documentation while the project continues to develop.", s["CellX"])],
    ]
    story += [make_table(status, [1.55*inch, 1.35*inch, 4.35*inch]), PageBreak()]

    # Page 2: methods and measured results.
    story += [
        p("1. Data, methodology, and results", s["SectionX"]),
        p("Dataset and preparation", s["SubsectionX"]),
        p("The experiment uses NASA's Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) turbofan degradation data. FD001 contains 100 training engines and 100 test engines under one operating condition and one simulated fault mode. Each cycle includes three operating settings and 21 sensor measurements. Training RUL is calculated from the final cycle of each engine and capped at 125 cycles; negative predictions are clipped to zero.", s["BodyX"]),
        p("Feature design and evaluation", s["SubsectionX"]),
        p("The model uses 67 inputs: cycle number, three operating settings, 21 current sensor values, and five-cycle rolling means and standard deviations for each sensor. Rolling summaries are calculated within each engine using only current and previous measurements. Ridge uses standardized inputs with alpha 10. Random Forest uses 250 trees, minimum leaf size 2, max_features 0.8, and seed 42. Validation uses one 80/20 engine-grouped split; the 20 held-out engines are scored at their final observed cycle. The selected model is refit on all FD001 training data and scored on the official test set's 100 engines.", s["BodyX"]),
        p("Evaluation results", s["SubsectionX"]),
    ]
    results = [[p("Evaluation", s["CellHeadX"]), p("Model", s["CellHeadX"]), p("Engines", s["CellHeadX"]), p("MAE", s["CellHeadX"]), p("RMSE", s["CellHeadX"]), p("NASA score", s["CellHeadX"])]]
    for label, model_name, count, metric in [
        ("Validation", "Ridge", m["validation_engines"], m["validation"]["ridge"]),
        ("Validation", "Random Forest", m["validation_engines"], m["validation"]["random_forest"]),
        ("Official FD001 test", "Random Forest", m["test_engines"], m["test"]),
    ]:
        results.append([p(label, s["CellX"]), p(model_name, s["CellX"]), p(str(count), s["CellX"]), p(f"{metric['mae']:.2f}", s["CellX"]), p(f"{metric['rmse']:.2f}", s["CellX"]), p(f"{metric['nasa_score']:.2f}", s["CellX"])])
    story += [make_table(results, [1.05*inch, 1.2*inch, .55*inch, 1.0*inch, 1.0*inch, 1.2*inch])]
    story += [
        p("Interpretation", s["SubsectionX"]),
        p("On validation engines, Random Forest reduced MAE from 4.44 to 1.89 cycles versus Ridge. On the official test engines, its MAE was 13.83 cycles, about 7.3 times the validation MAE. The gap is the main issue to investigate; the current experiment does not establish its cause. MAE and RMSE are measured in cycles. The asymmetric NASA score gives a larger penalty to overestimating remaining life; lower scores are better and the summed score depends on the number of engines.", s["BodyX"]),
    ]
    scatter_path = RESULTS / "fd001_test_scatter.png"
    if scatter_path.exists():
        im = Image(str(scatter_path), width=4.15*inch, height=2.8*inch)
        im.hAlign = "CENTER"
        story += [im, p("Figure 1. Predicted versus actual RUL for the official FD001 test engines; the dashed line is ideal prediction.", s["SmallX"])]
    story.append(PageBreak())

    # Page 3: limitations, remaining work, repository, references.
    story += [
        p("2. Remaining work and project status", s["SectionX"]),
        p("The first end-to-end baseline shows that the data and model pipeline can produce RUL estimates and benchmark metrics. The official test result indicates that generalization is not yet reliable, so further work is needed before drawing a strong conclusion about predictive performance.", s["BodyX"]),
        p("Limitations", s["SubsectionX"]),
        p("The experiments cover FD001 only, which represents one simulated operating condition and one fault mode. Validation currently uses one engine-level split. Evaluation measures a single final-cycle prediction per engine rather than performance throughout each trajectory. The benchmark is simulated and does not establish performance or safety for real aircraft. The models have not yet had broad hyperparameter tuning, temporal-model comparison, or uncertainty analysis.", s["BodyX"]),
        p("Remaining work", s["SubsectionX"]),
        p("- Analyze errors by engine and actual RUL range; verify target and test-label alignment.<br/>- Repeat engine-grouped validation and tune a limited set of baseline parameters.<br/>- Evaluate an additional C-MAPSS subset and, if scope permits, compare a temporal model.<br/>- Add error-analysis plots and strengthen the conclusions around generalization.<br/>- Refine reproducibility notes and continue improving the project code.", s["BodyX"]),
        p("Completion estimate", s["SubsectionX"]),
        p("The project is estimated to be <b>40% complete</b> and is still in progress. This estimate reflects the proposal, working data pipeline, initial model comparison, and first evaluation. Error analysis, robust validation, broader experiments, and final refinement remain.", s["BodyX"]),
        p("Code repository and reproducibility", s["SubsectionX"]),
        p("Public GitHub repository: <link href='https://github.com/kaushikkakad/PDS-project' color='#147D92'>kaushikkakad/PDS-project</link>. To reproduce the baseline, install requirements.txt, run python scripts/download_data.py, and then run python -m src.train. Raw benchmark data and the fitted model are excluded from Git.", s["BodyX"]),
        p("References", s["SubsectionX"]),
        p("1. Saxena, A., &amp; Goebel, K. (2008). <i>Turbofan Engine Degradation Simulation Data Set</i>. NASA Ames Prognostics Data Repository. <link href='https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/' color='#147D92'>NASA PCoE repository</link>.", s["SmallX"]),
        p("2. Tippareddy, S. (2024). <i>Predicting Remaining Useful Life of Turbofan Engines on C-MAPSS and N-CMAPSS Using Deep Recurrent Neural Networks</i>. San Jose State University, Master's Project. Listed in the supplied proposal.", s["SmallX"]),
        p("3. Heimes, F. O. (2008). <i>Recurrent Neural Networks for Remaining Useful Life Estimation</i>. International Conference on Prognostics and Health Management. Listed in the supplied proposal; verify full proceedings details against its bibliography.", s["SmallX"]),
        p("4. NASA Open Data Portal. <i>C-MAPSS Aircraft Engine Simulator Data</i>. <link href='https://data.nasa.gov/dataset/c-mapss-aircraft-engine-simulator-data' color='#147D92'>Dataset description</link>.", s["SmallX"]),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()

