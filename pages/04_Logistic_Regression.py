import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Logistic Regression")
st.write("Compare the three reported workflows, while keeping model specification and threshold differences visible.")

data = pd.DataFrame([
    {"Workflow": "Human", "Threshold": "0.0425", "Sensitivity": 0.8560, "Specificity": 0.6985, "Accuracy": 0.7064, "ROC-AUC": None, "PR-AUC": None},
    {"Workflow": "Data Analyst GPT", "Threshold": "0.4478 (exploratory)", "Sensitivity": 0.8468, "Specificity": 0.6848, "Accuracy": 0.6929, "ROC-AUC": 0.8332, "PR-AUC": 0.1867},
    {"Workflow": "Standard GPT", "Threshold": "0.4605 (exploratory)", "Sensitivity": 0.8226, "Specificity": 0.6992, "Accuracy": 0.7053, "ROC-AUC": 0.8311, "PR-AUC": 0.1827},
])
st.caption("Human values are from the human logistic-regression report. AI values are from the newer AI reports. The specifications differ, so this is a descriptive comparison, not a perfectly controlled head-to-head test.")
st.dataframe(
    data.style.format({"Sensitivity":"{:.1%}", "Specificity":"{:.1%}", "Accuracy":"{:.1%}", "ROC-AUC":"{:.3f}", "PR-AUC":"{:.3f}"}),
    use_container_width=True, hide_index=True
)

plot_data = data.melt(id_vars="Workflow", value_vars=["Sensitivity","Specificity","Accuracy"], var_name="Metric", value_name="Score")
fig = px.bar(plot_data, x="Workflow", y="Score", color="Metric", barmode="group", range_y=[0,1], title="Reported operating-point metrics")
st.plotly_chart(fig, use_container_width=True, key="lr_operating_point_chart")

st.header("Interpretation")
st.markdown("""
- **Sensitivity** measures the share of actual stroke cases detected at the chosen threshold.
- **Specificity** measures the share of non-stroke cases correctly classified.
- **Accuracy** is not sufficient by itself when the positive class is rare.
- The AI reports select a Youden threshold using the test ROC data and explicitly describe this as exploratory. For a final evaluation, select a threshold on training/validation data and evaluate it once on an untouched test set.
""")

st.header("Model specification caveat")
st.warning(
    "Specifications differ across workflows. The human values shown are from the "
    "main-effects Youden operating point (the human writeup prefers the interaction "
    "model for interpretation). Data Analyst GPT values are from the tuned balanced "
    "model that excludes work_type. Standard GPT values are from a tuned balanced "
    "model that retains work_type. Thresholds labeled exploratory were selected using "
    "test ROC information. Do not interpret this table as a controlled comparison of "
    "identical specifications."
)

st.subheader("Predictor findings")
st.markdown("""
Across the AI reports, age has the strongest reported association among the standardized numeric predictors, while BMI is not statistically significant in those tuned models. The human interaction model includes age × BMI and BMI × average-glucose terms, so its coefficients must be interpreted conditionally rather than as simple standalone effects.
""")
