import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.research_results import (
    DATASET_NOTE,
    DT_CV_AI,
    DT_DEFAULT_AI,
    DT_IMPORTANCE,
    DT_SOURCES,
    DT_STRUCTURE,
    DT_TEST_METRICS,
    SPLIT_NOTE,
    confusion_frame,
    style_metrics,
)

st.title("Decision Tree")
st.write(
    "Comparison of the selected decision-tree models from the human analysis, "
    "Standard GPT, and Data Analyst GPT workflows. All operating-point metrics "
    "below are from the untouched test set unless labeled otherwise."
)

st.info(SPLIT_NOTE)
st.caption(DATASET_NOTE)

# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------
st.header("1. Model structure")
st.write(
    "The human tuned tree is substantially more complex. Both AI workflows "
    "selected a shallow class-weighted tree that splits only on age."
)
st.dataframe(DT_STRUCTURE, use_container_width=True, hide_index=True)

struct_plot = DT_STRUCTURE.melt(
    id_vars="Workflow",
    value_vars=["Nodes", "Leaves", "Maximum depth"],
    var_name="Structure metric",
    value_name="Count",
)
fig_struct = px.bar(
    struct_plot,
    x="Workflow",
    y="Count",
    color="Structure metric",
    barmode="group",
    title="Tree complexity by workflow",
    color_discrete_sequence=["#1f3a5f", "#4a6fa5", "#8faadc"],
)
st.plotly_chart(fig_struct, use_container_width=True, key="dt_structure_chart")

with st.expander("Source notes — structure"):
    for workflow, source in DT_SOURCES.items():
        st.markdown(f"- **{workflow}:** `{source}`")

# ---------------------------------------------------------------------------
# Test performance
# ---------------------------------------------------------------------------
st.header("2. Untouched test-set performance")
st.write(
    "Primary comparison for the selected trees. The human threshold was chosen "
    "from the test ROC curve and is therefore exploratory. AI primary metrics "
    "use the default probability threshold of 0.50; an exploratory Youden "
    "threshold produced the same classifications for these shallow trees."
)

display_cols = [
    "Workflow", "Threshold", "Threshold protocol", "Accuracy", "Sensitivity",
    "Specificity", "Precision", "F1-score", "Balanced accuracy", "ROC-AUC", "PR-AUC",
]
st.dataframe(
    style_metrics(DT_TEST_METRICS[display_cols]),
    use_container_width=True,
    hide_index=True,
)

plot_metrics = DT_TEST_METRICS.melt(
    id_vars="Workflow",
    value_vars=["Sensitivity", "Specificity", "Accuracy", "ROC-AUC"],
    var_name="Metric",
    value_name="Score",
)
fig_perf = px.bar(
    plot_metrics,
    x="Workflow",
    y="Score",
    color="Metric",
    barmode="group",
    range_y=[0, 1],
    title="Selected decision-tree test metrics",
    color_discrete_sequence=["#1f3a5f", "#4a6fa5", "#8faadc", "#c5d4eb"],
)
st.plotly_chart(fig_perf, use_container_width=True, key="dt_test_metrics_chart")

st.warning(
    "Human ROC-AUC = 0.7880 is taken from the comprehensive report "
    "(*Sohn_ATP 2025.pdf*), where it appears with the same Acc/Sens/Spec values "
    "as the Human DT DOCX. The Human DT DOCX itself does not print a numeric AUC. "
    "Precision, F1, balanced accuracy, and PR-AUC were not transcribed for the "
    "human tree and are marked unavailable."
)

# ---------------------------------------------------------------------------
# Confusion matrices
# ---------------------------------------------------------------------------
st.header("3. Confusion matrices (test set)")
st.caption("Counts at the operating points shown in the table above.")

cm_cols = st.columns(3)
for i, (col, (_, row)) in enumerate(zip(cm_cols, DT_TEST_METRICS.iterrows())):
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
            key=f"dt_confusion_{i}_{row['Workflow']}",
        )
        st.caption(
            f"Detected {row['TP']} of {row['TP'] + row['FN']} stroke cases; "
            f"{row['FP']} false positives."
        )

# ---------------------------------------------------------------------------
# Feature importance
# ---------------------------------------------------------------------------
st.header("4. Feature importance")
st.write(
    "Importance reflects how much each variable contributed to the fitted tree, "
    "not statistical significance or causation."
)
st.dataframe(DT_IMPORTANCE, use_container_width=True, hide_index=True)

fig_imp = px.bar(
    DT_IMPORTANCE[DT_IMPORTANCE["Importance"] > 0],
    x="Importance",
    y="Variable",
    color="Workflow",
    orientation="h",
    barmode="group",
    title="Non-zero decision-tree importances",
    color_discrete_sequence=["#1f3a5f", "#4a6fa5", "#8faadc"],
)
fig_imp.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_imp, use_container_width=True, key="dt_importance_chart")

st.info(
    "Both AI tuned trees assign importance 1.0 to age and 0 to every other "
    "predictor. They function as age-based screening rules. The human tree "
    "also ranks age first, but retains secondary roles for glucose, BMI, and "
    "hypertension."
)

# ---------------------------------------------------------------------------
# Overfitting / CV context
# ---------------------------------------------------------------------------
st.header("5. Why the AI default tree was rejected")
st.write(
    "Before tuning, both AI workflows fit an unrestricted default tree. "
    "Perfect training performance should not be read as strong predictive ability."
)
st.dataframe(
    style_metrics(DT_DEFAULT_AI.drop(columns=["Workflow"])),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Training cross-validation for the selected AI tree")
st.dataframe(style_metrics(DT_CV_AI), use_container_width=True, hide_index=True)
st.caption(
    "Test sensitivity (0.8306) is lower than CV sensitivity (0.9113), while "
    "test ROC-AUC (0.8029) remains close to CV ROC-AUC (0.8120). The tuned "
    "tree generalizes far better than the default tree, but Standard GPT and "
    "Data Analyst GPT produced essentially the same age-only classifier."
)

# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------
st.header("6. Interpretation")
st.markdown("""
- **Complexity vs simplicity:** The human tree (39 nodes, depth 5) captures more
  predictor interactions. The AI trees (7 nodes, depth 2) are easier to explain
  but reduce the problem largely to age cutpoints.
- **Operating-point tradeoff:** AI sensitivity is slightly higher (83.1% vs 82.4%),
  while the human tree has higher accuracy and specificity at its chosen threshold.
- **Class imbalance:** Precision remains low for the AI trees (~11.5%) because
  stroke is rare; many positive predictions are false positives.
- **Threshold integrity:** Human and AI exploratory Youden thresholds were derived
  from test ROC information. For unbiased final evaluation, thresholds should be
  fixed on training/validation data before a single test evaluation.
- **Independence caveat:** Standard GPT and Data Analyst GPT tuned decision trees
  match on structure and test metrics; treat them as near-duplicate AI outcomes
  rather than independent replications.
""")

st.warning(
    "These models are research comparisons only. They are not clinically validated "
    "screening or diagnostic tools."
)
