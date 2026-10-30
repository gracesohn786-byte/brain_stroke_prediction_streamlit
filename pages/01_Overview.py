import streamlit as st

st.markdown("""
<div class="hero">
<h1>AI vs. Human: Data-Driven Prediction Model for Brain Stroke</h1>
<p>A research project comparing human-led statistical analysis with AI-assisted workflows for stroke prediction.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.subheader("Research question")
st.write("How do human-driven analysis, standard GPT, and Data Analyst GPT compare when building and interpreting predictive models for brain-stroke data?")

a, b, c = st.columns(3)
a.metric("Dataset size", "4,981", help="Reported in the AI logistic-regression reports; verify against the final source dataset.")
b.metric("Stroke prevalence", "≈ 5%", help="The outcome is imbalanced: most observations are non-stroke cases.")
c.metric("Workflows", "3", help="Human, standard GPT, and Data Analyst GPT.")

st.subheader("Project goals")
st.markdown("""
- Compare modeling workflows across logistic regression, decision trees, and random forests.
- Examine predictive performance using more than accuracy alone.
- Evaluate how model complexity, transparency, and reproducibility differ across workflows.
- Identify why AI-generated code and interpretations require independent statistical validation.
""")

st.subheader("Main takeaway")
st.info("AI can accelerate data analysis, but it cannot replace statistical validation. A faster workflow is useful only when its assumptions, code, metrics, and interpretations are checked.")

st.caption("Research project: Grace Sohn · Bridgewater State University · ATP, 2026")
st.warning("This site is a research presentation, not a clinical decision-support tool. The models are not validated for diagnosis or individual medical decisions.")
