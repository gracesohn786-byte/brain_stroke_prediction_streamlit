import streamlit as st

st.title("AI Reliability & Validation")
st.write(
    "This page summarizes reliability issues observed in the AI-assisted "
    "workflows for this project, based on the decision-tree, random-forest, "
    "and logistic-regression reports."
)

st.subheader("What AI contributed")
st.markdown("""
- Faster drafting of analysis code, tables, and explanatory text
- Structured multi-step modeling pipelines with saved metrics and figures
- Useful first-pass exploratory plots and, for Data Analyst GPT, an interactive EDA dashboard
""")

st.subheader("Project-specific findings")
st.markdown("""
1. **Near-duplicate decision trees.** Standard GPT and Data Analyst GPT both
   selected a depth-2, class-weighted, age-only tree with identical test
   metrics (ROC-AUC 0.8029, sensitivity 0.8306). Similar prompts can yield
   nearly the same model rather than independent analytical perspectives.

2. **Default trees overfit.** Unrestricted AI decision trees achieved perfect
   training metrics (accuracy/ROC-AUC = 1.0) with 359 nodes and depth 18, then
   collapsed on the test set (sensitivity ≈ 0.19, ROC-AUC ≈ 0.57). Perfect
   training fit is not evidence of predictive strength.

3. **Threshold protocol errors.** The comprehensive report documents cases
   where AI workflows appeared to treat an ROC false-positive-rate coordinate
   as a classification threshold. Separately, poster-era “AI random forest”
   metrics used a **test-set Youden** threshold on an **untuned** forest.
   Thresholds chosen on the test set are exploratory and should not be sold
   as unbiased final validation.

4. **Version mixing.** Data Analyst GPT’s tuned random forest selected
   threshold 0.47 by training CV, but saved test evaluations and the final
   model-comparison report emphasize 0.35. Publishing requires explicit model
   version and threshold labels.

5. **Specification drift.** AI logistic models used class-weighted, tuned
   estimators and different predictor sets (Standard GPT retained `work_type`;
   Data Analyst no-work_type models excluded it). Human models emphasized
   statistical inference. Metric tables are descriptive comparisons, not
   controlled experiments with identical specifications.

6. **Split and documentation inconsistencies.** Human and AI 50/50 splits are
   not identical. Human reports also list 4,891 observations in places while
   the dataset file contains 4,981. Small documentation errors reduce trust
   even when model code runs.
""")

st.subheader("Why human review remains essential")
st.markdown("""
- Generated code can implement a different model than the research question requires.
- Accuracy alone is misleading under ~5% stroke prevalence.
- Feature importance is not statistical significance or causation.
- Reproducibility depends on saved splits, seeds, thresholds, and exact model objects.
- Conceptual mistakes (for example, misreading ROC coordinates) can coexist with
  code that executes without errors.
""")

st.subheader("Validation checklist")
checks = [
    "Confirm dataset row count (4,981) and stroke count (248).",
    "Record each workflow's predictors, preprocessing, and class-weight settings.",
    "Keep training, cross-validation, and test roles separate.",
    "Choose thresholds on training/validation data; label any test-derived threshold as exploratory.",
    "Report sensitivity, specificity, precision, ROC-AUC, and PR-AUC where available.",
    "Distinguish default vs tuned models, and poster-era vs current results.",
    "Verify confusion matrices and metric calculations independently.",
    "Do not claim clinical readiness from this academic comparison.",
]
for i, item in enumerate(checks):
    st.checkbox(item, key=f"check_{i}")

st.info(
    "The project's central conclusion is not that AI is always worse. "
    "AI can accelerate analysis, but reliable conclusions still depend on "
    "validation, transparent labeling of evaluation protocols, and careful "
    "human interpretation."
)
