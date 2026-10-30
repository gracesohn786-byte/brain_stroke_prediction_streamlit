import streamlit as st
from pathlib import Path

st.title("Conclusion & Resources")

st.header("Main findings")
st.markdown("""
1. **AI accelerates workflow construction**, but human review remains necessary
   to verify splits, thresholds, model versions, and statistical interpretation.
2. **Decision trees diverged mainly in complexity.** The human tuned tree used
   multiple predictors (39 nodes, depth 5). Both AI workflows selected a shallow
   age-only tree (7 nodes, depth 2) with nearly identical test metrics.
3. **Random-forest comparisons depend on model version and threshold.** Poster
   “AI RF” metrics match a Data Analyst baseline forest with an exploratory test
   threshold. Tuned Standard GPT and Data Analyst forests differ in weighting,
   depth, and operating-point tradeoffs.
4. **Accuracy is misleading** under ~5% stroke prevalence. Default 0.50
   thresholds can appear accurate while missing most stroke cases.
5. **Reliability issues were concrete**, not abstract: overfitting default trees,
   test-set threshold selection, threshold/protocol mismatches, and occasional
   documentation inconsistencies (including the 4,891 vs 4,981 row-count typo).
""")

st.header("Limitations")
st.markdown("""
- Human and AI train/test partitions are not identical.
- Model specifications are not fully matched across workflows.
- Some human reports omit numeric ROC-AUC / PR-AUC values that AI CSVs include.
- No external validation cohort was used.
- The study does not establish clinical utility.
""")

st.header("Implications")
st.markdown("""
AI-assisted analysis is most useful as a drafting and organization tool.
Publication-quality conclusions still require independent checking of code,
evaluation design, and interpretation—especially for imbalanced medical outcomes.
""")

st.header("Research materials")
st.write(
    "Place public or shareable report files in the `assets/` folder. "
    "Avoid committing private or restricted data."
)
report_path = Path("assets/comprehensive_report.pdf")
uploaded = Path(__file__).resolve().parents[1] / "assets" / "Sohn_ATP_2025.pdf"
pdf_path = report_path if report_path.exists() else uploaded
if pdf_path.exists():
    st.download_button(
        "Download comprehensive report (PDF)",
        pdf_path.read_bytes(),
        file_name="Sohn_ATP_2025.pdf",
        mime="application/pdf",
    )
else:
    st.caption(
        "Add the final PDF as `assets/comprehensive_report.pdf` or "
        "`assets/Sohn_ATP_2025.pdf` to enable download."
    )

st.subheader("References and disclosures")
st.markdown("""
- Project report: *AI vs. Human: Data-Driven Prediction Model for Brain Stroke*
  (ATP / Bridgewater State University).
- Human DT/RF reports; Standard GPT and Data Analyst GPT DT/RF reports; Data
  Analyst final model-comparison report.
- Tableau Public dashboards: see Exploratory Analysis.
- Dataset: cite the original public provider and license in the final publication package.
""")
st.warning(
    "The project is for research and educational purposes. It is not a clinically "
    "validated screening or diagnostic system."
)
