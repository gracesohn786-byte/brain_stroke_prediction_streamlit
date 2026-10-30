import streamlit as st

st.set_page_config(
    page_title="AI vs. Human | Brain Stroke Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}
    .hero {padding: 2rem; border-radius: 18px; background: linear-gradient(120deg,#eaf2ff,#f7f9fc); border: 1px solid #dce6f4;}
    .hero h1 {font-size: 2.5rem; margin-bottom: .4rem; color: #142744;}
    .hero p {font-size: 1.1rem; color: #344761;}
    div[data-testid="stMetric"] {background: #f8fafc; border: 1px solid #e5eaf1; padding: 1rem; border-radius: 12px;}
</style>
<style>
/* Sidebar section headers */
[data-testid="stSidebarNav"] li:has(a[href="#"]) span {
    font-weight: 700 !important;
}
/* Alternative selectors for Streamlit versions */
[data-testid="stSidebarNav"] [role="heading"] {
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

overview = st.Page("pages/01_Overview.py", title="Overview", icon="", default=True)
method = st.Page("pages/02_Data_and_Methodology.py", title="Data & Methodology", icon="")
eda = st.Page("pages/03_Exploratory_Analysis.py", title="Exploratory Analysis", icon="")
logistic = st.Page("pages/04_Logistic_Regression.py", title="Logistic Regression", icon="")
tree = st.Page("pages/05_Decision_Tree.py", title="Decision Tree", icon="")
forest = st.Page("pages/06_Random_Forest.py", title="Random Forest", icon="")
reliability = st.Page("pages/07_AI_Reliability.py", title="AI Reliability", icon="")
conclusion = st.Page("pages/08_Conclusion_and_Resources.py", title="Conclusion & Resources", icon="")

pg = st.navigation({
    "Research": [overview, method, eda],
    "Model comparisons": [logistic, tree, forest],
    "Discussion": [reliability, conclusion],
})
pg.run()
