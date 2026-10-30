import streamlit as st

st.title("Data & Methodology")
st.write(
    "This page summarizes the study design used for the human vs AI comparison "
    "of brain-stroke prediction models."
)

st.header("Dataset")
st.markdown("""
The analysis uses a public brain-stroke dataset with **4,981** observations and
**11** variables:

- Gender, age, hypertension, heart disease, ever married, work type,
  residence type, average glucose level, BMI, smoking status
- Outcome: stroke (0 = no stroke, 1 = stroke)

There are **248** stroke cases (**≈4.98%**). The outcome is highly imbalanced,
so accuracy alone is not an adequate performance summary.

Some human-written reports list 4,891 observations. The CSV count of **4,981**
is preferred.
""")

st.header("Train / test split")
st.markdown("""
Each workflow used an approximately 50/50 train–test partition:

| Workflow | Train | Test | Stroke cases (train / test) |
|---|---:|---:|---|
| Human | 2,491 | 2,490 | 123 / 125 |
| Standard GPT & Data Analyst GPT | 2,490 | 2,491 | 124 / 124 |

These partitions are **not identical**. Cross-workflow metric differences
partly reflect split differences as well as modeling choices.
""")

st.header("Three analysis workflows")
st.dataframe([
    {
        "Workflow": "Human analysis",
        "Approach": "Human-led R and Python analysis, manual code review, "
                    "statistical interpretation, and Tableau visualization.",
    },
    {
        "Workflow": "Standard GPT",
        "Approach": "General ChatGPT workflow with researcher-supplied prompts; "
                    "saved stepwise metrics for logistic regression, decision tree, "
                    "and random forest.",
    },
    {
        "Workflow": "Data Analyst GPT",
        "Approach": "Data-analysis-oriented GPT workflow with researcher-supplied "
                    "prompts; structured preprocessing, tuning, and evaluation reports.",
    },
], use_container_width=True, hide_index=True)

st.header("Model families")
st.markdown("""
1. **Logistic regression** — association estimates and probability prediction.
2. **Decision tree** — inspectable rule-based splits.
3. **Random forest** — ensemble of trees for prediction and variable importance.
""")

st.header("Evaluation principles")
st.markdown("""
- Distinguish **training**, **cross-validation**, and **untouched test** results.
- Prefer sensitivity, specificity, precision, balanced accuracy, ROC-AUC, and
  PR-AUC over accuracy alone.
- Label classification thresholds and whether they were selected on training/CV
  data or exploratorily on the test set.
- Interpret feature importance as model contribution, not causation or
  statistical significance.
- Do not claim clinical readiness from this academic comparison.
""")
