"""
Verified Decision Tree and Random Forest results for publication display.

Every numeric value is traced to a named source. Values that cannot be
confirmed from primary reports are set to None and must not be invented.
Human and AI workflows used different 50/50 partitions, so comparisons
are descriptive rather than a controlled head-to-head experiment.
"""

from __future__ import annotations

import pandas as pd

# ---------------------------------------------------------------------------
# Shared caveats
# ---------------------------------------------------------------------------

SPLIT_NOTE = (
    "Human analyses used a 50/50 split of approximately 2,491 train / 2,490 test "
    "observations (123 / 125 stroke cases). AI workflows used approximately "
    "2,490 train / 2,491 test (124 stroke cases each). The partitions are not "
    "identical, so metric differences partly reflect split differences as well "
    "as modeling choices."
)

DATASET_NOTE = (
    "The source dataset contains 4,981 observations and 248 stroke cases "
    "(≈4.98%). Some human-written reports incorrectly list 4,891 observations; "
    "the CSV count of 4,981 is preferred."
)

# ---------------------------------------------------------------------------
# Decision Tree
# ---------------------------------------------------------------------------

DT_SOURCES = {
    "Human": "Human-driven analysis/decision_tree/report/Decision Tree Results.docx; "
             "comprehensive report Sohn_ATP 2025.pdf §4.2 for ROC-AUC 0.7880",
    "Standard GPT": "AI-driven analysis/Standard ChatGPT/Decision Tree/"
                    "decision_tree_stroke_analysis_report_v1_9.docx and "
                    "8_Evaluation/tuned_decision_tree_test_metrics.csv",
    "Data Analyst GPT": "AI-driven analysis/Data Analyst GPT/Decision Tree/"
                        "decision_tree_analysis_report_final.docx and "
                        "8_Evaluation/tuned_decision_tree_test_metrics.csv",
}

# Final selected trees for publication comparison
DT_STRUCTURE = pd.DataFrame([
    {
        "Workflow": "Human",
        "Selected model": "Tuned tree (Python Model #3)",
        "Nodes": 39,
        "Leaves": 20,
        "Maximum depth": 5,
        "Class weight": "None",
        "Key settings": "min_samples_split=10, min_samples_leaf=5, ccp_alpha=0.0001",
        "Root / main split": "Age (human report: age ≤ 73.5)",
    },
    {
        "Workflow": "Standard GPT",
        "Selected model": "Class-weighted Model B",
        "Nodes": 7,
        "Leaves": 4,
        "Maximum depth": 2,
        "Class weight": "balanced",
        "Key settings": "min_samples_split=10, min_samples_leaf=5, ccp_alpha=0.0",
        "Root / main split": "Age only (age-only tree)",
    },
    {
        "Workflow": "Data Analyst GPT",
        "Selected model": "Class-weighted Model B",
        "Nodes": 7,
        "Leaves": 4,
        "Maximum depth": 2,
        "Class weight": "balanced",
        "Key settings": "saved model: min_samples_split=2, min_samples_leaf=1, ccp_alpha=0.0",
        "Root / main split": "Age only (age-only tree)",
    },
])

# Untouched test-set operating points for the selected trees
DT_TEST_METRICS = pd.DataFrame([
    {
        "Workflow": "Human",
        "Evaluation set": "Test",
        "Threshold": 0.0512,
        "Threshold protocol": "Test-set Youden / best threshold (exploratory)",
        "Accuracy": 0.6916,
        "Sensitivity": 0.8240,
        "Specificity": 0.6846,
        "Precision": None,
        "F1-score": None,
        "Balanced accuracy": None,
        "ROC-AUC": 0.7880,  # comprehensive report; not numeric in Human DT DOCX
        "PR-AUC": None,
        "TN": 1619,
        "FP": 746,
        "FN": 22,
        "TP": 103,
        "ROC-AUC note": "Reported in Sohn_ATP 2025.pdf alongside matching Acc/Sens/Spec; "
                        "not transcribed in the Human DT DOCX text.",
    },
    {
        "Workflow": "Standard GPT",
        "Evaluation set": "Test",
        "Threshold": 0.50,
        "Threshold protocol": "Default 0.50 (primary)",
        "Accuracy": 0.6736250501806503,
        "Sensitivity": 0.8306451612903226,
        "Specificity": 0.6653992395437263,
        "Precision": 0.11508379888268157,
        "F1-score": 0.20215897939156036,
        "Balanced accuracy": 0.7480222004170245,
        "ROC-AUC": 0.8028673835125448,
        "PR-AUC": 0.14260437145897203,
        "TN": 1575,
        "FP": 792,
        "FN": 21,
        "TP": 103,
        "ROC-AUC note": None,
    },
    {
        "Workflow": "Data Analyst GPT",
        "Evaluation set": "Test",
        "Threshold": 0.50,
        "Threshold protocol": "Default 0.50 (primary)",
        "Accuracy": 0.6736250501806503,
        "Sensitivity": 0.8306451612903226,
        "Specificity": 0.6653992395437263,
        "Precision": 0.11508379888268157,
        "F1-score": 0.20215897939156036,
        "Balanced accuracy": 0.7480222004170245,
        "ROC-AUC": 0.8028673835125448,
        "PR-AUC": 0.14260437145897203,
        "TN": 1575,
        "FP": 792,
        "FN": 21,
        "TP": 103,
        "ROC-AUC note": None,
    },
])

# Default / preliminary AI trees (overfitting evidence)
DT_DEFAULT_AI = pd.DataFrame([
    {
        "Workflow": "Standard GPT / Data Analyst GPT (shared pattern)",
        "Stage": "Default unpruned tree — apparent training",
        "Nodes": 359,
        "Leaves": 180,
        "Maximum depth": 18,
        "Accuracy": 1.0,
        "Sensitivity": 1.0,
        "Specificity": 1.0,
        "ROC-AUC": 1.0,
        "PR-AUC": 1.0,
        "Note": "Perfect training fit is not evidence of generalization.",
    },
    {
        "Workflow": "Standard GPT / Data Analyst GPT (shared pattern)",
        "Stage": "Default unpruned tree — untouched test @ 0.50",
        "Nodes": 359,
        "Leaves": 180,
        "Maximum depth": 18,
        "Accuracy": 0.9161,
        "Sensitivity": 0.1855,
        "Specificity": 0.9544,
        "ROC-AUC": 0.5699,
        "PR-AUC": 0.0731,
        "Note": "Large drop from training performance indicates overfitting.",
    },
])

DT_IMPORTANCE = pd.DataFrame([
    {"Workflow": "Human", "Rank": 1, "Variable": "age", "Importance": 0.4521},
    {"Workflow": "Human", "Rank": 2, "Variable": "avg_glucose_level", "Importance": 0.1770},
    {"Workflow": "Human", "Rank": 3, "Variable": "bmi", "Importance": 0.1762},
    {"Workflow": "Human", "Rank": 4, "Variable": "hypertension", "Importance": 0.0588},
    {"Workflow": "Human", "Rank": 5, "Variable": "work_type (Private)", "Importance": 0.0392},
    {"Workflow": "Standard GPT", "Rank": 1, "Variable": "age", "Importance": 1.0},
    {"Workflow": "Standard GPT", "Rank": 2, "Variable": "(all others)", "Importance": 0.0},
    {"Workflow": "Data Analyst GPT", "Rank": 1, "Variable": "age", "Importance": 1.0},
    {"Workflow": "Data Analyst GPT", "Rank": 2, "Variable": "(all others)", "Importance": 0.0},
])

DT_CV_AI = pd.DataFrame([
    {
        "Workflow": "Standard GPT / Data Analyst GPT",
        "Evaluation set": "Training CV (Model B)",
        "Accuracy": 0.6699,
        "Sensitivity": 0.9113,
        "Specificity": 0.6572,
        "Precision": 0.1223,
        "F1-score": 0.2156,
        "Balanced accuracy": 0.7843,
        "ROC-AUC": 0.8120,
        "PR-AUC": 0.1382,
    },
])

# ---------------------------------------------------------------------------
# Random Forest
# ---------------------------------------------------------------------------

RF_SOURCES = {
    "Human": "Human-driven analysis/random_forest/Random Forest results.docx "
             "(Python tuned model); Sohn_ATP 2025.pdf §4.3",
    "Standard GPT": "AI-driven analysis/Standard ChatGPT/Random Forest/"
                    "random_forest_stroke_analysis_report_v1_3.docx and "
                    "Tuned model CSV metrics",
    "Data Analyst GPT": "AI-driven analysis/Data Analyst GPT/Random forest/"
                        "random_forest_analysis_report_step4.docx and "
                        "Tuned model CSV metrics",
}

RF_STRUCTURE = pd.DataFrame([
    {
        "Workflow": "Human",
        "Selected model": "Tuned balanced RF (Python)",
        "n_estimators": 100,
        "max_depth": 6,
        "Class weight": "balanced",
        "Other settings": "random_state=42, Gini, max_features=√p",
        "OOB accuracy": 0.9592,
        "Notes": "R implementation used class weights 1:19 and unlimited depth; "
                 "Python metrics are preferred for the website comparison.",
    },
    {
        "Workflow": "Standard GPT",
        "Selected model": "Custom weight 1:10 RF",
        "n_estimators": 120,
        "max_depth": 5,
        "Class weight": "{0: 1, 1: 10}",
        "Other settings": "min_samples_split=10, min_samples_leaf=10, max_features=sqrt",
        "OOB accuracy": None,
        "Notes": "Training-CV threshold = 0.35 (selected without using the test set).",
    },
    {
        "Workflow": "Data Analyst GPT",
        "Selected model": "Large-leaf balanced RF",
        "n_estimators": 100,
        "max_depth": 6,
        "Class weight": "balanced",
        "Other settings": "min_samples_split=20, min_samples_leaf=20, max_features=sqrt",
        "OOB accuracy": None,
        "Notes": "Training-CV threshold = 0.47; final comparison / test files also "
                 "report a user-specified threshold of 0.35.",
    },
])

# Primary test-set comparison for tuned models
RF_TEST_METRICS = pd.DataFrame([
    {
        "Workflow": "Human",
        "Model version": "Tuned balanced RF (Python)",
        "Evaluation set": "Test",
        "Threshold": 0.0721,
        "Threshold protocol": "Test-set Youden / best threshold (exploratory)",
        "Accuracy": 0.7020,
        "Sensitivity": 0.8080,
        "Specificity": 0.6964,
        "Precision": None,
        "F1-score": None,
        "Balanced accuracy": None,
        "ROC-AUC": 0.8120,  # Sohn_ATP 2025.pdf
        "PR-AUC": None,
        "TN": 1647,
        "FP": 718,
        "FN": 24,
        "TP": 101,
    },
    {
        "Workflow": "Standard GPT",
        "Model version": "Tuned custom-weight 1:10 RF",
        "Evaluation set": "Test",
        "Threshold": 0.35,
        "Threshold protocol": "Training-CV selected (unbiased relative to test)",
        "Accuracy": 0.7406663990365315,
        "Sensitivity": 0.7661290322580645,
        "Specificity": 0.739332488381918,
        "Precision": 0.13342696629213482,
        "F1-score": 0.22727272727272727,
        "Balanced accuracy": 0.7527307603199913,
        "ROC-AUC": 0.8206539515106914,
        "PR-AUC": 0.17772238754058842,
        "TN": 1750,
        "FP": 617,
        "FN": 29,
        "TP": 95,
    },
    {
        "Workflow": "Data Analyst GPT",
        "Model version": "Tuned large-leaf balanced RF",
        "Evaluation set": "Test",
        "Threshold": 0.35,
        "Threshold protocol": "User-specified / final-comparison threshold "
                              "(CV selected 0.47; test metrics at 0.47 unavailable)",
        "Accuracy": 0.6772380570052188,
        "Sensitivity": 0.8306451612903226,
        "Specificity": 0.6692015209125475,
        "Precision": 0.1162528216704289,
        "F1-score": 0.20396039603960395,
        "Balanced accuracy": 0.749923341101435,
        "ROC-AUC": 0.8148346893440724,
        "PR-AUC": 0.16813631871766382,
        "TN": 1584,
        "FP": 783,
        "FN": 21,
        "TP": 103,
    },
])

# Additional RF rows for threshold context (not the primary comparison)
RF_THRESHOLD_CONTEXT = pd.DataFrame([
    {
        "Workflow": "Human",
        "Model version": "Tuned balanced RF (Python)",
        "Threshold": 0.50,
        "Threshold protocol": "Default 0.50",
        "Accuracy": 0.7884,
        "Sensitivity": 0.656,
        "Specificity": 0.7953,
        "ROC-AUC": None,
        "Note": "Higher accuracy than the Youden operating point, but lower stroke sensitivity.",
    },
    {
        "Workflow": "Standard GPT",
        "Model version": "Tuned custom-weight 1:10 RF",
        "Threshold": 0.50,
        "Threshold protocol": "Default 0.50",
        "Accuracy": 0.8783621035728623,
        "Sensitivity": 0.41935483870967744,
        "Specificity": 0.9024081115335868,
        "ROC-AUC": 0.8206539515106914,
        "Note": "Default threshold misses many stroke cases despite high accuracy.",
    },
    {
        "Workflow": "Data Analyst GPT",
        "Model version": "Tuned large-leaf balanced RF",
        "Threshold": 0.50,
        "Threshold protocol": "Default 0.50",
        "Accuracy": 0.762745885186672,
        "Sensitivity": 0.7096774193548387,
        "Specificity": 0.7655259822560203,
        "ROC-AUC": 0.8148346893440724,
        "Note": "Default 0.50 is closer to a balanced operating point than in the Standard GPT tuned RF.",
    },
    {
        "Workflow": "Data Analyst GPT",
        "Model version": "Tuned large-leaf balanced RF",
        "Threshold": 0.47,
        "Threshold protocol": "Training-CV selected",
        "Accuracy": 0.7461847389558233,
        "Sensitivity": 0.8064516129032258,
        "Specificity": 0.7430262045646661,
        "ROC-AUC": 0.8238826929893928,
        "Note": "These metrics are from training CV, not the untouched test set. "
                "Test metrics at 0.47 were not saved in the available CSVs.",
    },
])

# Poster / comprehensive-report historical comparison (DA baseline RF)
RF_HISTORICAL = pd.DataFrame([
    {
        "Workflow": "Human (Python tuned)",
        "Model version": "Tuned balanced RF",
        "Threshold": 0.0721,
        "Threshold protocol": "Test Youden (exploratory)",
        "Accuracy": 0.7020,
        "Sensitivity": 0.8080,
        "Specificity": 0.6964,
        "ROC-AUC": 0.8120,
    },
    {
        "Workflow": "Data Analyst GPT (baseline / default)",
        "Model version": "Untuned RF (500 trees, no class weight)",
        "Threshold": 0.042,
        "Threshold protocol": "Exploratory test Youden",
        "Accuracy": 0.7109594540345243,
        "Sensitivity": 0.8145161290322581,
        "Specificity": 0.7055344317701732,
        "ROC-AUC": 0.80060339070826,
    },
])

RF_IMPORTANCE = pd.DataFrame([
    {"Workflow": "Human", "Rank": 1, "Variable": "age", "Importance": 0.4892},
    {"Workflow": "Human", "Rank": 2, "Variable": "avg_glucose_level", "Importance": 0.1272},
    {"Workflow": "Human", "Rank": 3, "Variable": "bmi", "Importance": 0.1054},
    {"Workflow": "Human", "Rank": 4, "Variable": "hypertension", "Importance": 0.0613},
    {"Workflow": "Human", "Rank": 5, "Variable": "ever_married (Yes)", "Importance": 0.0562},
    {"Workflow": "Standard GPT", "Rank": 1, "Variable": "age", "Importance": 0.4880},
    {"Workflow": "Standard GPT", "Rank": 2, "Variable": "avg_glucose_level", "Importance": 0.1371},
    {"Workflow": "Standard GPT", "Rank": 3, "Variable": "ever_married", "Importance": 0.0806},
    {"Workflow": "Standard GPT", "Rank": 4, "Variable": "bmi", "Importance": 0.0755},
    {"Workflow": "Standard GPT", "Rank": 5, "Variable": "hypertension", "Importance": 0.0605},
    {"Workflow": "Data Analyst GPT", "Rank": 1, "Variable": "age", "Importance": 0.5180},
    {"Workflow": "Data Analyst GPT", "Rank": 2, "Variable": "avg_glucose_level", "Importance": 0.1186},
    {"Workflow": "Data Analyst GPT", "Rank": 3, "Variable": "ever_married", "Importance": 0.0910},
    {"Workflow": "Data Analyst GPT", "Rank": 4, "Variable": "bmi", "Importance": 0.0748},
    {"Workflow": "Data Analyst GPT", "Rank": 5, "Variable": "work_type", "Importance": 0.0545},
])

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

PCT_COLS = [
    "Accuracy", "Sensitivity", "Specificity", "Precision",
    "F1-score", "Balanced accuracy", "OOB accuracy",
]
AUC_COLS = ["ROC-AUC", "PR-AUC"]


def style_metrics(df: pd.DataFrame) -> "pd.io.formats.style.Styler":
    """Format percentage and AUC columns for Streamlit display."""
    fmt: dict[str, str] = {}
    for col in PCT_COLS:
        if col in df.columns:
            fmt[col] = "{:.1%}"
    for col in AUC_COLS:
        if col in df.columns:
            fmt[col] = "{:.4f}"
    if "Threshold" in df.columns:
        fmt["Threshold"] = "{:.4f}"
    return df.style.format(fmt, na_rep="Unavailable")


def confusion_frame(row: pd.Series) -> pd.DataFrame:
    """Build a 2×2 confusion matrix from TN/FP/FN/TP fields."""
    return pd.DataFrame(
        [[int(row["TN"]), int(row["FP"])],
         [int(row["FN"]), int(row["TP"])]],
        index=["Actual no stroke", "Actual stroke"],
        columns=["Predicted no stroke", "Predicted stroke"],
    )
