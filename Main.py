import streamlit as st
import pandas as pd
import numpy as np
import random

# -------------------------------
# 🧬 Simulated Genetic Algorithm Using CSV Dataset
# -------------------------------
def run_genetic_algorithm_with_data(co_r, mut_r, data):
    """
    Simulate a GA that selects the best program for each hour
    based on modified ratings and random variation.
    """

    # Identify hour columns
    hour_cols = [col for col in data.columns if "Modified Hour" in col]

    schedule = []
    for hour in hour_cols:
        # Select program with the best rating (plus random variation)
        data["Score"] = data[hour] + np.random.uniform(-mut_r, mut_r, len(data))
        best_program = data.loc[data["Score"].idxmax(), "Type of Program"]
        best_score = data.loc[data["Score"].idxmax(), hour]

        schedule.append({"Hour": hour.replace("Modified ", ""), 
                         "Program": best_program, 
                         "Fitness Score": round(best_score, 2)})

    return pd.DataFrame(schedule)

# -------------------------------
# 🎛️ Streamlit Interface
# -------------------------------
st.title("Genetic Algorithm Scheduler with Real Dataset")

st.write("""
This app uses a **Genetic Algorithm** concept to generate a program schedule 
based on your uploaded dataset and chosen parameters.
""")

# Upload CSV
uploaded_file = st.file_uploader("Upload the program ratings CSV file", type=["csv"])

# Input sliders for parameters
co_r = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8, 0.01)
mut_r = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, 0.01)

# Display chosen parameters
st.subheader("Selected Parameters")
st.write(f"**Crossover Rate (CO_R):** {co_r}")
st.write(f"**Mutation Rate (MUT_R):** {mut_r}")

# Run GA if file uploaded
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("✅ Dataset successfully loaded!")
    st.dataframe(data.head())

    if st.button("Run Genetic Algorithm"):
        st.info("Running Genetic Algorithm... Please wait...")

        # Run GA using uploaded dataset
        schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data)

        # Display schedule table
        st.subheader("📅 Generated Program Schedule")
        st.dataframe(schedule_df, use_container_width=True)

        # Summary statistics
        st.subheader("📊 Summary")
        st.write(f"Total Hours Scheduled: {len(schedule_df)}")
        st.write(f"Unique Programs: {schedule_df['Program'].nunique()}")

else:
    st.warning("⚠️ Please upload the modified program ratings CSV file first.")
