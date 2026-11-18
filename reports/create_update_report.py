"""Create an evidence-based project status report PDF without a work timeline."""
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
    styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=21, leading=25, alignment=1, textColor=NAVY, spaceAfter=9))
    styles.add(ParagraphStyle(name="Subtitle", parent=styles["Heading2"], fontName="Helvetica", fontSize=13, leading=17, alignment=1, textColor=INK, spaceAfter=9))
    styles.add(ParagraphStyle(name="SectionX", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY, spaceBefore=8, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle(name="SubsectionX", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=TEAL, spaceBefore=6, spaceAfter=3, keepWithNext=True))
    styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.1, leading=13, textColor=INK, spaceAfter=6))
    styles.add(ParagraphStyle(name="SmallX", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.7, leading=10, textColor=MUTED, spaceAfter=4))
    styles.add(ParagraphStyle(name="CellX", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.8, leading=10, textColor=INK))
    styles.add(ParagraphStyle(name="CellHeadX", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.7, leading=9, textColor=colors.white))
    styles.add(ParagraphStyle(name="Status", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=18, alignment=1, textColor=TEAL, spaceBefore=3, spaceAfter=9))
    return styles


def para(text, style):
    return Paragraph(text, style)


def table(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#C8D5DA")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, PALE]),
    ]
    if header:
        commands.extend([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)])
    t.setStyle(TableStyle(commands))
    return t


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CAD6DC"))
    canvas.line(.62*inch, .43*inch, 7.88*inch, .43*inch)
    canvas.setFont("Helvetica", 8)
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
        topMargin=.55*inch, bottomMargin=.60*inch,
        title="Project Update Report - Predictive Maintenance of Aircraft Turbofan Engines",
        author="Kaushik Kakad",
    )
    story = []

    story += [
        para("PROJECT UPDATE REPORT", s["Cover"]),
        para("Predictive Maintenance of Aircraft Turbofan Engines Using Machine Learning", s["Subtitle"]),
        para("Prepared by Kaushik Kakad", s["BodyX"]),
        para("ESTIMATED PROJECT COMPLETION: 40%", s["Status"]),
        para("Executive summary", s["SectionX"]),
        para("This project investigates whether turbofan engine sensor measurements can estimate remaining useful life (RUL) and support condition-based maintenance planning. The project has moved from proposal framing into implementation and preliminary modeling. A reproducible FD001 data pipeline and two baseline models are in place, with results measured on engine-level validation data and the official test set. The current overall completion estimate is 40%. Substantial work remains in error analysis, robust evaluation, model improvement, broader comparisons, and final documentation.", s["BodyX"]),
        para("Project objective and working questions", s["SectionX"]),
        para("<b>Objective.</b> Build and evaluate machine-learning approaches that estimate the number of cycles remaining before simulated turbofan failure, then assess how the prediction errors may affect maintenance planning.", s["BodyX"]),
        para("The following working questions formalize the direction set in the original proposal:", s["BodyX"]),
        para("1. Can operating settings and sensor histories predict turbofan remaining useful life?  2. How does a tree ensemble compare with a regularized linear baseline?  3. How well do validation results carry over to official test engines?  4. What additional checks are needed before these estimates could support maintenance decisions?", s["BodyX"]),
        para("Work completed and remaining", s["SectionX"]),
    ]
    progress_rows = [
        [para("Component", s["CellHeadX"]), para("Current status", s["CellHeadX"]), para("Evidence or remaining work", s["CellHeadX"])],
        [para("Proposal and research framing", s["CellX"]), para("Complete", s["CellX"]), para("The project problem, objective, working questions, and initial references are established in the proposal.", s["CellX"])],
        [para("Dataset and preprocessing", s["CellX"]), para("Implemented for FD001", s["CellX"]), para("Loads NASA C-MAPSS, creates RUL labels, and generates engine-specific rolling sensor features.", s["CellX"])],
        [para("Baseline modeling", s["CellX"]), para("Initial comparison complete", s["CellX"]), para("Ridge regression and Random Forest have been trained and compared.", s["CellX"])],
        [para("Evaluation and interpretation", s["CellX"]), para("Preliminary", s["CellX"]), para("Initial validation and test scores are available. The validation-to-test gap still needs investigation and robust repeated validation.", s["CellX"])],
        [para("Extension and finalization", s["CellX"]), para("In progress", s["CellX"]), para("Evaluate more subsets or model families, complete error analysis, refine conclusions, and maintain the public code repository.", s["CellX"])],
    ]
    story += [table(progress_rows, [1.45*inch, 1.4*inch, 4.4*inch]), PageBreak()]

    story += [
        para("1. Data and methodology", s["SectionX"]),
        para("Dataset", s["SubsectionX"]),
        para("The experiment uses NASA's Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) Turbofan Engine Degradation Simulation data. The simulator produces run-to-failure training trajectories and separate test trajectories that stop before failure. The FD001 subset contains 100 training engines and 100 test engines under one operating condition and one simulated fault mode. Each cycle contains an engine identifier, cycle count, three operating settings, and 21 sensor measurements. The official RUL file supplies remaining cycles beyond each test trajectory's last observed cycle.", s["BodyX"]),
        para("Preprocessing and target", s["SubsectionX"]),
        para("For each training engine, cycle-level RUL is computed as the engine's final training cycle minus the current cycle. Training RUL is capped at 125 cycles. Predictions below zero are clipped to zero. Engine ID is used to keep cycles grouped during validation, but it is not passed to the prediction model.", s["BodyX"]),
        para("Feature engineering", s["SubsectionX"]),
        para("The 67 model inputs consist of cycle number, three operating settings, 21 current sensor values, and two trailing summaries for each sensor: a five-cycle rolling mean and standard deviation. Each rolling window is calculated within one engine and uses only current and previous observations. At the beginning of an engine's sequence, the window uses the available history; a standard deviation with fewer than two observations is set to zero.", s["BodyX"]),
        para("Models and evaluation", s["SubsectionX"]),
    ]
    method_rows = [
        [para("Item", s["CellHeadX"]), para("Implementation", s["CellHeadX"])],
        [para("Ridge regression", s["CellX"]), para("StandardScaler followed by Ridge regression (alpha = 10), used as a regularized linear baseline.", s["CellX"])],
        [para("Random Forest", s["CellX"]), para("250 trees; minimum leaf size 2; max_features = 0.8; random seed 42.", s["CellX"])],
        [para("Validation", s["CellX"]), para("One 80/20 GroupShuffleSplit by engine (seed 42). All cycles from 80 engines train the models; the 20 held-out engines are scored at their final observed cycle.", s["CellX"])],
        [para("Official test", s["CellX"]), para("The selected model is refit on all FD001 training cycles and scored on the final observed cycle of each of the 100 official test engines.", s["CellX"])],
    ]
    story += [table(method_rows, [1.35*inch, 5.9*inch]), para("Evaluation metrics", s["SubsectionX"])]
    story += [para("MAE reports the average absolute prediction error in cycles. RMSE gives more weight to larger errors. The asymmetric NASA score sums an exponential penalty per engine and penalizes overestimation of RUL (predicting more remaining life than is available) more steeply. Lower values are better. The NASA score is a sum, so it depends on the number of evaluated engines and should only be compared across equivalent sets.", s["BodyX"]), PageBreak()]

    story += [
        para("2. Preliminary experimental results", s["SectionX"]),
        para("Random Forest achieved the lowest validation MAE and was selected for the FD001 test evaluation. It performed better than Ridge on the held-out validation engines, but substantially worse on the separate official test set.", s["BodyX"]),
    ]
    result_rows = [[para("Evaluation", s["CellHeadX"]), para("Model", s["CellHeadX"]), para("Engines", s["CellHeadX"]), para("MAE (cycles)", s["CellHeadX"]), para("RMSE (cycles)", s["CellHeadX"]), para("NASA score", s["CellHeadX"])]]
    for label, model_name, count, metric in [
        ("Validation", "Ridge", m["validation_engines"], m["validation"]["ridge"]),
        ("Validation", "Random Forest", m["validation_engines"], m["validation"]["random_forest"]),
        ("Official FD001 test", "Random Forest", m["test_engines"], m["test"]),
    ]:
        result_rows.append([para(label, s["CellX"]), para(model_name, s["CellX"]), para(str(count), s["CellX"]), para(f"{metric['mae']:.2f}", s["CellX"]), para(f"{metric['rmse']:.2f}", s["CellX"]), para(f"{metric['nasa_score']:.2f}", s["CellX"])])
    story += [table(result_rows, [.98*inch, 1.15*inch, .55*inch, 1.15*inch, 1.2*inch, 1.17*inch]), Spacer(1, 5)]
    story += [
        para("Validation comparison", s["SubsectionX"]),
        para("On the 20 held-out validation engines, Random Forest reduced MAE from 4.44 to 1.89 cycles compared with Ridge. RMSE fell from 7.55 to 2.20 cycles, and the NASA score fell from 18.44 to 4.32. This indicates that the nonlinear ensemble fits the validation trajectories better under this split.", s["BodyX"]),
        para("Generalization finding", s["SubsectionX"]),
        para("On the official FD001 test engines, Random Forest MAE was 13.83 cycles, RMSE was 18.87 cycles, and NASA score was 632.61. Test MAE is about 7.3 times validation MAE. This is the main issue to investigate. The current evidence does not establish the cause; analysis should check errors by engine and RUL range, target alignment, feature distributions, and sensitivity to validation splits.", s["BodyX"]),
    ]
    scatter_path = RESULTS / "fd001_test_scatter.png"
    if scatter_path.exists():
        im = Image(str(scatter_path), width=4.55*inch, height=3.07*inch)
        im.hAlign = "CENTER"
        story += [im, para("Figure 1. Predicted versus actual RUL on the 100-engine official FD001 test set. The dashed line shows ideal predictions.", s["SmallX"])]
    story.append(PageBreak())

    story += [
        para("3. Interpretation, limitations, and remaining work", s["SectionX"]),
        para("Interpretation", s["SubsectionX"]),
        para("The end-to-end baseline demonstrates that the project can load the data, construct RUL targets, train models, and produce benchmark metrics. The validation result alone makes Random Forest appear strong, while the official test result shows that generalization is not yet reliable. The project should therefore focus next on diagnosing the gap and strengthening evaluation before drawing a broad conclusion about predictive performance.", s["BodyX"]),
        para("Limitations", s["SubsectionX"]),
        para("The experiments cover only FD001, one simulated operating condition and one fault mode. Validation currently uses one engine-level split, so its results may depend on which engines were held out. Evaluation measures one final-cycle prediction per engine rather than prediction quality throughout each trajectory. The benchmark is simulated and does not establish performance on real aircraft or safety for operational maintenance. The models have not yet undergone broad hyperparameter search, temporal-model comparison, or uncertainty analysis.", s["BodyX"]),
        para("Remaining work", s["SubsectionX"]),
        para("- Analyze residuals by engine and actual RUL range, and verify target/test-label alignment.<br/>- Repeat engine-grouped validation with multiple splits and tune a limited set of baseline parameters.<br/>- Evaluate at least one additional C-MAPSS subset and compare a temporal model if the remaining scope allows.<br/>- Add error-analysis plots and explain the generalization gap in the conclusions.<br/>- Complete reproducibility notes and keep the report consistent with the public code repository.", s["BodyX"]),
        para("Progress estimate", s["SubsectionX"]),
        para("The project is currently estimated to be <b>40% complete</b>. The estimate reflects completed proposal framing, a working FD001 preprocessing pipeline, an initial model comparison, and first validation/test results. The remaining analysis, robustness work, model extensions, and final polishing represent the larger unfinished portion of the project.", s["BodyX"]),
        para("Reproducibility and repository", s["SubsectionX"]),
        para("The code is available in the public <link href='https://github.com/kaushikkakad/PDS-project' color='#147D92'>kaushikkakad/PDS-project</link> repository. To reproduce the baseline, install packages from requirements.txt, run python scripts/download_data.py, and then run python -m src.train. The script saves metrics, predictions, plots, and a fitted model locally. Raw benchmark data and the model binary are excluded from Git.", s["BodyX"]),
        para("References", s["SubsectionX"]),
        para("1. Saxena, A., &amp; Goebel, K. (2008). <i>Turbofan Engine Degradation Simulation Data Set</i>. NASA Ames Prognostics Data Repository, NASA Ames Research Center. <link href='https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/' color='#147D92'>NASA PCoE dataset repository</link>.", s["SmallX"]),
        para("2. Tippareddy, S. (2024). <i>Predicting Remaining Useful Life of Turbofan Engines on C-MAPSS and N-CMAPSS Using Deep Recurrent Neural Networks</i>. San Jose State University, Master's Project. Listed in the supplied project proposal.", s["SmallX"]),
        para("3. Heimes, F. O. (2008). <i>Recurrent Neural Networks for Remaining Useful Life Estimation</i>. International Conference on Prognostics and Health Management. Listed in the supplied project proposal; verify full proceedings details against the original bibliography.", s["SmallX"]),
        para("4. NASA Open Data Portal. <i>C-MAPSS Aircraft Engine Simulator Data</i>. <link href='https://data.nasa.gov/dataset/c-mapss-aircraft-engine-simulator-data' color='#147D92'>Dataset description</link>.", s["SmallX"]),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()

