import streamlit as st
import pandas as pd
import numpy as np

# Load the axial length data
data = pd.read_excel("분석용.xlsx")  # Make sure this file is uploaded in the Streamlit app

st.set_page_config(page_title="Axial Length Percentile Calculator")
st.title("Axial Length Percentile Checker")
st.markdown("Enter your information to find out the percentile of your axial length compared to population data.")

# User inputs
sex = st.selectbox("Select your sex", options=["M", "F"])
age = st.selectbox("Select your age", options=sorted(data['age'].unique()))
axial_length = st.number_input("Enter your Axial Length (in mm)", min_value=15.0, max_value=30.0, step=0.01)

if st.button("Check Percentile"):
    # Filter data by age and sex
    filtered = data[(data['age'] == age) & (data['sex'] == sex)]['axial length']

    if len(filtered) < 10:
        st.warning("Not enough data available for this age and sex group to calculate a reliable percentile.")
    else:
        # Calculate percentile
        percentile_rank = round(stats.percentileofscore(filtered, axial_length, kind='rank'), 2)

        # Determine percentile band
        bands = [5, 10, 25, 50, 75, 90, 95]
        labels = ['<5th', '5-10th', '10-25th', '25-50th', '50-75th', '75-90th', '90-95th', '>95th']
        bins = [-np.inf] + list(np.percentile(filtered, bands)) + [np.inf]
        band = labels[np.digitize(axial_length, bins) - 1]

        st.success(f"Your axial length is in the **{band}** percentile band.")
        st.info(f"Exact percentile: **{percentile_rank}**")
