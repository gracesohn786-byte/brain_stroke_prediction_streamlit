# Brain Stroke Research — Streamlit Site

A multipage Streamlit site for presenting the research project *AI vs. Human: Data-Driven Prediction Model for Brain Stroke*.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Publish on Streamlit Community Cloud

1. Create a GitHub repository and upload this project folder.
2. Add the final public/shareable report to `assets/comprehensive_report.pdf` if appropriate.
3. Open `pages/03_Exploratory_Analysis.py` and set the Tableau Public dashboard URL as the default value, or keep the URL input editable.
4. Go to https://share.streamlit.io/ and sign in with GitHub.
5. Select **Create app**, choose the repository, branch, and `streamlit_app.py`.
6. Deploy. Streamlit will install dependencies from `requirements.txt`.

## Before publishing

- Verify all metrics against the final report.
- Confirm dataset counts and stroke prevalence; one report has an inconsistent row-count statement.
- Label model versions and specifications clearly.
- Do not use test data to select the final classification threshold.
- Confirm Tableau dashboards are publicly viewable.
- Do not upload identifiable or restricted data.
- Include citations for the dataset and any reused figures.

## Current implementation notes

The project contains pages for overview, data/methodology, exploratory analysis, logistic regression, decision tree, random forest, AI reliability, and conclusions. The logistic page preserves the human / Data Analyst GPT / standard GPT distinction and flags specification differences. Decision-tree and random-forest results should be checked against the final source reports before final release.
