import streamlit as st

st.title("Exploratory Data Analysis")
st.write(
    "Explore the project's Tableau dashboards. Use the selector to switch between "
    "the overview, descriptive statistics, charts, categorical dashboard, and multivariable dashboard."
)

DASHBOARDS = {
    "Home": "https://public.tableau.com/views/StrokeDataVisualizations_17749728802740/Home?:showVizHome=no",
    "Descriptive stats": "https://public.tableau.com/views/StrokeDataVisualizations_17749728802740/Descriptivestats?:showVizHome=no",
    "Charts": "https://public.tableau.com/views/StrokeDataVisualizations_17749728802740/Charts?:showVizHome=no",
    "Categorical dashboard": "https://public.tableau.com/views/StrokeDataVisualizations_17749728802740/cat_dashboard?:showVizHome=no",
    "Multivariable dashboard": "https://public.tableau.com/views/StrokeDataVisualizations_17749728802740/multvar_dashboard?:showVizHome=no",
}

choice = st.selectbox("Choose a Tableau dashboard", list(DASHBOARDS.keys()))
st.subheader(choice)
st.components.v1.iframe(DASHBOARDS[choice], height=850, scrolling=True)

with st.expander("Having trouble viewing a dashboard?"):
    st.write(
        "The Tableau workbook must be publicly accessible on Tableau Public for an embedded view to load. "
        "If it prompts for authentication or appears blank, open it directly using the link below."
    )
    st.markdown(f"[Open {choice} on Tableau Public]({DASHBOARDS[choice].split('?:')[0]})")

st.caption(
    "These dashboards are embedded from Tableau Public. Interactive filters and tooltips may be available "
    "inside the embedded view."
)
