"""Create a detailed, evidence-based project update report PDF."""
from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

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
    styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=21, leading=25, alignment=TA_CENTER, textColor=NAVY, spaceAfter=9))
    styles.add(ParagraphStyle(name="Subtitle", parent=styles["Heading2"], fontName="Helvetica", fontSize=13, leading=17, alignment=TA_CENTER, textColor=INK, spaceAfter=9))
    styles.add(ParagraphStyle(name="SectionX", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY, spaceBefore=8, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle(name="SubsectionX", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=TEAL, spaceBefore=6, spaceAfter=3, keepWithNext=True))
    styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.1, leading=13, textColor=INK, spaceAfter=6))
    styles.add(ParagraphStyle(name="SmallX", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.7, leading=10, textColor=MUTED, spaceAfter=4))
    styles.add(ParagraphStyle(name="CellX", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.8, leading=10, textColor=INK))
    styles.add(ParagraphStyle(name="CellHeadX", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.7, leading=9, textColor=colors.white))
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
    canvas.drawString(.62*inch, .27*inch, "Aircraft Turbofan Predictive Maintenance | Progress update: November 17, 2026")
    canvas.drawRightString(7.88*inch, .27*inch, f"Page {document.page}")
    canvas.restoreState()


def main():
    m = json.loads(METRICS.read_text())
    s = styleset()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, rightMargin=.62*inch, leftMargin=.62*inch,
        topMargin=.55*inch, bottomMargin=.60*inch,
        title="Detailed Project Update - Predictive Maintenance of Aircraft Turbofan Engines",
        author="Kaushik Kakad",
    )
    story = []

    # Page 1: truthful timeline, project framing, and status.
    story += [
        para("PROJECT UPDATE REPORT", s["Cover"]),
        para("Predictive Maintenance of Aircraft Turbofan Engines Using Machine Learning", s["Subtitle"]),
        para("Prepared by Kaushik Kakad | Status as of November 17, 2026", s["BodyX"]),
        para("Executive summary", s["SectionX"]),
        para("The project studies whether sensor measurements from an aircraft turbofan can be used to estimate remaining useful life (RUL) and support condition-based maintenance planning. The work available before this update was proposal-level: it described the maintenance problem, stated the project direction, and identified prior work. A reproducible software baseline was started on November 15, 2026. This report separates that new implementation from the earlier proposal and reports only measured results from the current run.", s["BodyX"]),
        para("Project objective and questions", s["SectionX"]),
        para("<b>Objective.</b> Build and evaluate machine-learning methods that use engine sensor sequences to estimate the cycles remaining before simulated failure, then assess how prediction errors could inform maintenance planning.", s["BodyX"]),
        para("The following working questions formalize the proposal's direction:", s["BodyX"]),
        para("1. Can operating settings and sensor histories predict turbofan remaining useful life?  2. How does a tree ensemble compare with a regularized linear baseline?  3. How well do validation results carry over to the official test engines?  4. Which additional checks are needed before treating the estimates as useful maintenance decision support?", s["BodyX"]),
        para("Progress timeline", s["SectionX"]),
    ]
    status_rows = [
        [para("Work area", s["CellHeadX"]), para("Status and timing", s["CellHeadX"]), para("Evidence / next action", s["CellHeadX"])],
        [para("Proposal framing", s["CellX"]), para("Completed before Nov. 15", s["CellX"]), para("Problem, project objective, guiding questions, and initial references are in the supplied proposal. This update does not attribute the new code or experiments to that earlier period.", s["CellX"])],
        [para("Dataset and pipeline", s["CellX"]), para("Started and implemented Nov. 15", s["CellX"]), para("Downloaded NASA C-MAPSS; added FD001 loading, RUL labels, and rolling sensor features.", s["CellX"])],
        [para("Initial model run", s["CellX"]), para("Completed Nov. 15", s["CellX"]), para("Compared Ridge and Random Forest; evaluated held-out engines and official FD001 test engines.", s["CellX"])],
        [para("Further analysis and repository", s["CellX"]), para("Analysis pending; repo created Nov. 17", s["CellX"]), para("Investigate the validation-to-test gap and improve the experiment. Public project repository: kaushikkakad/PDS-project.", s["CellX"])],
    ]
    story.append(table(status_rows, [1.25*inch, 1.45*inch, 4.55*inch]))
    story += [Spacer(1, 5), para("The course notice originally provided with the project listed November 10, 2026, while the student now identifies approximately December 1, 2026, as the current deadline. Confirm the active date and late-submission instructions in the course site before submitting.", s["SmallX"]), PageBreak()]

    # Page 2: data and reproducible method.
    story += [
        para("1. Data and methodology", s["SectionX"]),
        para("Dataset", s["SubsectionX"]),
        para("The experiment uses NASA's Commercial Modular Aero-Propulsion System Simulation (C-MAPSS) Turbofan Engine Degradation Simulation data. The simulator produces run-to-failure training trajectories and separate test trajectories that stop before failure. The FD001 subset contains 100 training engines and 100 test engines under one operating condition and one simulated fault mode. Each cycle contains an engine identifier, cycle count, three operating settings, and 21 sensor measurements. The official RUL file supplies the remaining cycles beyond each test trajectory's last observed cycle.", s["BodyX"]),
        para("Preprocessing and target", s["SubsectionX"]),
        para("For each training engine, cycle-level RUL is computed as the engine's final training cycle minus the current cycle. To follow a common C-MAPSS modeling convention and reduce the influence of very early-life labels, training RUL is capped at 125 cycles. Predictions below zero are clipped to zero. Engine ID is used to keep cycles grouped during validation, but it is not passed to the prediction model.", s["BodyX"]),
        para("Feature engineering", s["SubsectionX"]),
        para("The 67 model inputs consist of cycle number, three operating settings, 21 current sensor values, and two trailing summaries for each sensor: a five-cycle rolling mean and standard deviation. The rolling window is calculated within each engine and includes only the current and previous observed cycles. At the start of an engine's sequence, the window uses the available history; the first standard deviation is set to zero when fewer than two samples exist.", s["BodyX"]),
        para("Models and evaluation protocol", s["SubsectionX"]),
    ]
    method_rows = [
        [para("Item", s["CellHeadX"]), para("Implementation", s["CellHeadX"])],
        [para("Ridge regression", s["CellX"]), para("StandardScaler followed by Ridge regression (alpha = 10). Provides a regularized linear baseline.", s["CellX"])],
        [para("Random Forest", s["CellX"]), para("250 trees; minimum leaf size 2; max_features = 0.8; random seed 42.", s["CellX"])],
        [para("Validation", s["CellX"]), para("One 80/20 GroupShuffleSplit by engine (seed 42). All cycles for 80 engines train the models; the 20 held-out engines are scored at their final observed cycle.", s["CellX"])],
        [para("Official test", s["CellX"]), para("The selected model is refit on all FD001 training cycles and scored on the last observed cycle of each of the 100 official test engines, using the supplied RUL labels.", s["CellX"])],
    ]
    story.append(table(method_rows, [1.35*inch, 5.9*inch]))
    story += [
        para("Metrics", s["SubsectionX"]),
        para("MAE is the mean absolute error in cycles and is easy to interpret as typical absolute miss. RMSE squares larger errors before averaging and is therefore more sensitive to large misses. The asymmetric NASA score sums an exponential penalty for each prediction error; overestimation of RUL (predicting more life than remains) receives the steeper penalty. Lower values are better for all three metrics. The NASA score is a sum over engines, so it depends on the number of evaluated engines and should be compared only across equivalent sets.", s["BodyX"]),
        PageBreak(),
    ]

    # Page 3: results and plots.
    story += [
        para("2. Preliminary results", s["SectionX"]),
        para("The Random Forest achieved the lowest validation MAE and was selected for the final FD001 run. It performed better than Ridge on the 20 held-out validation engines, but its performance was materially worse on the separate official test set.", s["BodyX"]),
    ]
    result_rows = [[para("Evaluation", s["CellHeadX"]), para("Model", s["CellHeadX"]), para("Engines", s["CellHeadX"]), para("MAE (cycles)", s["CellHeadX"]), para("RMSE (cycles)", s["CellHeadX"]), para("NASA score", s["CellHeadX"])]]
    for label, model_name, count, metric in [
        ("Validation", "Ridge", m["validation_engines"], m["validation"]["ridge"]),
        ("Validation", "Random Forest", m["validation_engines"], m["validation"]["random_forest"]),
        ("Official FD001 test", "Random Forest", m["test_engines"], m["test"]),
    ]:
        result_rows.append([para(label, s["CellX"]), para(model_name, s["CellX"]), para(str(count), s["CellX"]), para(f"{metric['mae']:.2f}", s["CellX"]), para(f"{metric['rmse']:.2f}", s["CellX"]), para(f"{metric['nasa_score']:.2f}", s["CellX"])])
    story += [table(result_rows, [.98*inch, 1.15*inch, .55*inch, 1.15*inch, 1.2*inch, 1.17*inch]), Spacer(1, 5)]
    story += [para("Validation comparison", s["SubsectionX"]), para("On the held-out validation engines, Random Forest reduced MAE from 4.44 to 1.89 cycles compared with Ridge. RMSE fell from 7.55 to 2.20 cycles, and the NASA score fell from 18.44 to 4.32. This suggests that the nonlinear ensemble fits the validation trajectories better than the linear baseline under this split.", s["BodyX"])]
    story += [para("Test-set generalization", s["SubsectionX"]), para("On the official FD001 test engines, Random Forest MAE was 13.83 cycles, RMSE was 18.87 cycles, and NASA score was 632.61. Test MAE is about 7.3 times the validation MAE. This is the main finding to investigate next. The current evidence does not establish the cause; possible checks include the RUL distribution, errors by engine and RUL range, implementation alignment with the benchmark protocol, and sensitivity to the single validation split.", s["BodyX"])]
    scatter_path = RESULTS / "fd001_test_scatter.png"
    if scatter_path.exists():
        im = Image(str(scatter_path), width=4.55*inch, height=3.07*inch)
        im.hAlign = "CENTER"
        story += [im, para("Figure 1. Predicted versus actual RUL on the 100-engine official FD001 test set. The dashed line is the ideal prediction.", s["SmallX"])]
    story.append(PageBreak())

    # Page 4: interpretation, limitations, plan, references.
    story += [
        para("3. Interpretation, limitations, and next steps", s["SectionX"]),
        para("Current interpretation", s["SubsectionX"]),
        para("The initial baseline confirms that the local data and modeling pipeline can produce RUL predictions and benchmark metrics end to end. The validation result alone would make the Random Forest look strong, but the official test result shows that the current model does not yet generalize consistently. The next update should treat error analysis and a more robust validation design as the central work, rather than presenting the first validation score as a final result.", s["BodyX"]),
        para("Limitations", s["SubsectionX"]),
        para("(1) Only FD001 has been run; it represents one simulated operating condition and one fault mode. (2) Validation uses one random engine split, so its result may vary with the split. (3) Evaluation uses one final-cycle prediction per engine and does not measure how predictions evolve throughout a trajectory. (4) The data is simulated; these results do not validate performance on real aircraft or establish maintenance safety. (5) The model has not yet been tuned through a systematic search, compared with temporal neural networks, or assessed with uncertainty estimates.", s["BodyX"]),
        para("Work plan through December 1", s["SubsectionX"]),
    ]
    plan_rows = [
        [para("Target window", s["CellHeadX"]), para("Planned work", s["CellHeadX"]), para("Deliverable", s["CellHeadX"])],
        [para("Nov. 18-20", s["CellX"]), para("Inspect prediction residuals by engine and actual RUL range; verify target and test-label alignment; summarize sensor and cycle distributions.", s["CellX"]), para("Error-analysis tables and a short diagnosis of the validation/test gap.", s["CellX"])],
        [para("Nov. 21-23", s["CellX"]), para("Run repeated engine-grouped validation splits; tune a small set of Random Forest parameters and retain the fixed official test set for final reporting.", s["CellX"]), para("Robust validation comparison and selected baseline settings.", s["CellX"])],
        [para("Nov. 23-26", s["CellX"]), para("Evaluate at least one additional C-MAPSS subset or implement a sequence-model comparison if time and dependencies allow.", s["CellX"]), para("Evidence on whether results transfer beyond FD001; document scope if this phase is reduced.", s["CellX"])],
        [para("Nov. 27-29", s["CellX"]), para("Finalize plots, explain findings and limitations, publish the source code, and insert the public repository URL.", s["CellX"]), para("Complete report and accessible code repository.", s["CellX"])],
        [para("Nov. 30-Dec. 1", s["CellX"]), para("Re-run the documented pipeline from a clean environment, check report links and figures, and submit through the course site.", s["CellX"]), para("Final PDF and GitHub link submitted by the course-site deadline.", s["CellX"])],
    ]
    story += [table(plan_rows, [1.0*inch, 3.65*inch, 2.6*inch]), Spacer(1, 5)]
    story += [
        para("Reproducibility and repository", s["SubsectionX"]),
        para("The project code is published in the public <link href='https://github.com/kaushikkakad/PDS-project' color='#147D92'>kaushikkakad/PDS-project</link> repository. To reproduce the current run: install packages from requirements.txt, run python scripts/download_data.py, then run python -m src.train. The script saves metrics, predictions, plots, and a fitted model under reports/generated/ and models/. Raw benchmark data and the model binary are excluded from Git.", s["BodyX"]),
        para("References", s["SubsectionX"]),
        para("1. Saxena, A., &amp; Goebel, K. (2008). <i>Turbofan Engine Degradation Simulation Data Set</i>. NASA Ames Prognostics Data Repository, NASA Ames Research Center. <link href='https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/' color='#147D92'>NASA PCoE dataset repository</link>.", s["SmallX"]),
        para("2. Tippareddy, S. (2024). <i>Predicting Remaining Useful Life of Turbofan Engines on C-MAPSS and N-CMAPSS Using Deep Recurrent Neural Networks</i>. San Jose State University, Master's Project. Reference listed in the supplied project proposal.", s["SmallX"]),
        para("3. Heimes, F. O. (2008). <i>Recurrent Neural Networks for Remaining Useful Life Estimation</i>. International Conference on Prognostics and Health Management. Reference listed in the supplied project proposal; verify final proceedings details against the original bibliography before submission.", s["SmallX"]),
        para("4. NASA Open Data Portal. <i>C-MAPSS Aircraft Engine Simulator Data</i>. <link href='https://data.nasa.gov/dataset/c-mapss-aircraft-engine-simulator-data' color='#147D92'>Dataset description</link>.", s["SmallX"]),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()

