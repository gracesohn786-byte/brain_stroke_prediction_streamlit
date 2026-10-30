import sys
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.research_results import (
    DATASET_NOTE,
    RF_HISTORICAL,
    RF_IMPORTANCE,
    RF_SOURCES,
    RF_STRUCTURE,
    RF_TEST_METRICS,
    RF_THRESHOLD_CONTEXT,
    SPLIT_NOTE,
    confusion_frame,
    style_metrics,
)

st.title("Random Forest")
st.write(
    "Comparison of selected random-forest models across the human analysis, "
    "Standard GPT, and Data Analyst GPT workflows. The primary table uses the "
    "tuned models. Poster-era metrics are retained separately because they "
    "refer to a different AI model version and threshold protocol."
)

st.info(SPLIT_NOTE)
st.caption(DATASET_NOTE)

# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------
st.header("1. Model configuration")
st.write(
    "All three selected forests address class imbalance, but they differ in "
    "tree count, depth limits, and weighting schemes."
)
st.dataframe(RF_STRUCTURE, use_container_width=True, hide_index=True)

with st.expander("Source notes — configuration"):
    for workflow, source in RF_SOURCES.items():
        st.markdown(f"- **{workflow}:** `{source}`")

# ---------------------------------------------------------------------------
# Primary test metrics
# ---------------------------------------------------------------------------
st.header("2. Primary test-set comparison (tuned models)")
st.write(
    "Use this table as the main three-workflow comparison. Threshold protocols "
    "differ and are labeled explicitly: the human operating point used a "
    "test-derived Youden threshold; Standard GPT used a training-CV threshold "
    "of 0.35; Data Analyst GPT's CV-selected threshold was 0.47, but the saved "
    "test evaluation and final model-comparison report use 0.35."
)

primary_cols = [
    "Workflow", "Model version", "Threshold", "Threshold protocol",
    "Accuracy", "Sensitivity", "Specificity", "Precision", "F1-score",
    "Balanced accuracy", "ROC-AUC", "PR-AUC",
]
st.dataframe(
    style_metrics(RF_TEST_METRICS[primary_cols]),
    use_container_width=True,
    hide_index=True,
)

plot_df = RF_TEST_METRICS.melt(
    id_vars="Workflow",
    value_vars=["Sensitivity", "Specificity", "Accuracy", "ROC-AUC"],
    var_name="Metric",
    value_name="Score",
)
fig_perf = px.bar(
    plot_df,
    x="Workflow",
    y="Score",
    color="Metric",
    barmode="group",
    range_y=[0, 1],
    title="Tuned random-forest test metrics at labeled operating points",
    color_discrete_sequence=["#1f3a5f", "#4a6fa5", "#8faadc", "#c5d4eb"],
)
st.plotly_chart(fig_perf, use_container_width=True, key="rf_test_metrics_chart")

st.warning(
    "Data Analyst GPT: training cross-validation selected threshold **0.47**, "
    "but the test CSV / final comparison report evaluate threshold **0.35**. "
    "Test metrics at 0.47 are unavailable in the saved files. Treat the 0.35 "
    "Data Analyst row as a documented operating point, not as proof that 0.35 "
    "was the CV-chosen cutoff."
)

# ---------------------------------------------------------------------------
# Confusion matrices
# ---------------------------------------------------------------------------
st.header("3. Confusion matrices (primary operating points)")
cm_cols = st.columns(3)
for i, (col, (_, row)) in enumerate(zip(cm_cols, RF_TEST_METRICS.iterrows())):
    with col:
        st.subheader(row["Workflow"])
        st.caption(f"Threshold {row['Threshold']:.4f}")
        cm = confusion_frame(row)
        fig_cm = go.Figure(
            data=go.Heatmap(
                z=cm.values,
                x=list(cm.columns),
                y=list(cm.index),
                colorscale="Blues",
                text=cm.values,
                texttemplate="%{text}",
                showscale=False,
            )
        )
        fig_cm.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(
            fig_cm,
            use_container_width=True,
            key=f"rf_confusion_{i}_{row['Workflow']}",
        )
        st.caption(
            f"Detected {row['TP']} of {int(row['TP'] + row['FN'])} stroke cases; "
            f"{row['FP']} false positives."
        )

# ---------------------------------------------------------------------------
# Threshold context
# ---------------------------------------------------------------------------
st.header("4. Threshold context")
st.write(
    "Classification metrics change sharply with the probability cutoff. "
    "Default 0.50 often looks accurate on this imbalanced dataset while "
    "missing many stroke cases."
)
st.dataframe(
    style_metrics(RF_THRESHOLD_CONTEXT),
    use_container_width=True,
    hide_index=True,
)

# ---------------------------------------------------------------------------
# Feature importance
# ---------------------------------------------------------------------------
st.header("5. Feature importance")
st.write(
    "Across workflows, age, average glucose level, and BMI remain among the "
    "leading contributors. Importance is model-associated, not causal."
)
st.dataframe(RF_IMPORTANCE, use_container_width=True, hide_index=True)

fig_imp = px.bar(
    RF_IMPORTANCE,
    x="Importance",
    y="Variable",
    color="Workflow",
    orientation="h",
    barmode="group",
    title="Top random-forest grouped importances",
    color_discrete_sequence=["#1f3a5f", "#4a6fa5", "#8faadc"],
)
fig_imp.update_layout(yaxis={"categoryorder": "total ascending"}, height=480)
st.plotly_chart(fig_imp, use_container_width=True, key="rf_importance_chart")

# ---------------------------------------------------------------------------
# Historical / poster
# ---------------------------------------------------------------------------
st.header("6. Historical poster / comprehensive-report comparison")
st.write(
    "The symposium poster and *Sohn_ATP 2025.pdf* compared the human tuned "
    "Python forest with the Data Analyst GPT **baseline** (untuned) forest "
    "at an exploratory test Youden threshold. Those numbers are preserved "
    "here for continuity, but they are **not** the tuned three-workflow "
    "comparison above."
)
st.dataframe(style_metrics(RF_HISTORICAL), use_container_width=True, hide_index=True)
st.caption(
    "Historical AI row = Data Analyst GPT baseline RF (500 trees, no class "
    "weight) at exploratory test threshold 0.042. At the default 0.50 "
    "threshold that same baseline model had sensitivity 0.0 on the test set."
)

# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------
st.header("7. Interpretation")
st.markdown("""
- **Why results differ:** Human and AI forests used different depth limits,
  tree counts, and class-weight schemes, and they were evaluated at different
  thresholds. Standard GPT's training-selected threshold (0.35) yields higher
  specificity and accuracy than Data Analyst GPT's reported 0.35 operating
  point, while Data Analyst GPT achieves higher sensitivity at that cutoff.
- **Thresholds matter more than headline accuracy:** At 0.50, accuracy can
  exceed 87–95% while stroke sensitivity collapses. Screening-oriented
  comparisons should emphasize sensitivity, specificity, precision, ROC-AUC,
  and PR-AUC together.
- **Human threshold caveat:** The human 0.0721 cutoff was chosen using test
  ROC information and is exploratory. It should not be described as an
  externally validated decision rule.
- **Data Analyst threshold conflict:** Prefer the training-CV threshold (0.47)
  for methodological cleanliness once test metrics at 0.47 are available; until
  then, keep 0.35 clearly labeled.
- **Discrimination:** Available ROC-AUC values are similar across tuned forests
  (~0.81–0.82). Differences in Acc/Sens/Spec are largely operating-point effects.
""")

st.warning(
    "These models are research comparisons only. They are not clinically validated "
    "screening or diagnostic tools."
)
