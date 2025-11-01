import streamlit as st
import pandas as pd
import numpy as np
 
# -----------------------------------
# 🧬 Genetic Algorithm Simulation
# -----------------------------------
def run_genetic_algorithm_with_data(co_r, mut_r, data):
    """
    Simulate a GA that selects the best program for each hour
    based on modified ratings and random variation.
    """

    hour_cols = [col for col in data.columns if "Modified Hour" in col]
    schedule = []

    for hour in hour_cols:
        # Add random variation to simulate mutation impact
        data["Score"] = data[hour] + np.random.uniform(-mut_r, mut_r, len(data))
        best_program = data.loc[data["Score"].idxmax(), "Type of Program"]
        best_score = data.loc[data["Score"].idxmax(), hour]

        schedule.append({
            "Hour": hour.replace("Modified ", ""),
            "Program": best_program,
            "Fitness Score": round(best_score, 2)
        })

    return pd.DataFrame(schedule)

# -----------------------------------
# 🎛️ Streamlit Interface
# -----------------------------------
st.title("Genetic Algorithm Scheduler – Multiple Trials")

st.write("""
Upload your **Program Ratings Dataset (CSV)** and run the **Genetic Algorithm** three times
with different Crossover and Mutation Rates to compare results.
""")

# Upload dataset
uploaded_file = st.file_uploader("Upload the modified program ratings CSV file", type=["csv"])

# Parameter input for 3 trials
st.subheader("⚙️ Set Parameters for Each Trial")

col1, col2 = st.columns(2)
with col1:
    co_r1 = st.slider("Trial 1 – Crossover Rate (CO_R)", 0.0, 0.95, 0.8, 0.01)
    mut_r1 = st.slider("Trial 1 – Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, 0.01)
    co_r2 = st.slider("Trial 2 – Crossover Rate (CO_R)", 0.0, 0.95, 0.6, 0.01)
    mut_r2 = st.slider("Trial 2 – Mutation Rate (MUT_R)", 0.01, 0.05, 0.03, 0.01)
with col2:
    co_r3 = st.slider("Trial 3 – Crossover Rate (CO_R)", 0.0, 0.95, 0.4, 0.01)
    mut_r3 = st.slider("Trial 3 – Mutation Rate (MUT_R)", 0.01, 0.05, 0.04, 0.01)

# Run all 3 trials
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.success("✅ Dataset successfully loaded!")

    if st.button("Run All Trials"):
        st.info("Running all 3 genetic algorithm trials...")

        trials = [
            ("Trial 1", co_r1, mut_r1),
            ("Trial 2", co_r2, mut_r2),
            ("Trial 3", co_r3, mut_r3)
        ]

        for name, co_r, mut_r in trials:
            st.subheader(f"🧬 {name}")
            st.write(f"**Parameters:** CO_R = {co_r}, MUT_R = {mut_r}")

            schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data)

            st.dataframe(schedule_df, use_container_width=True)

            st.write(f"**Summary:** {schedule_df['Program'].nunique()} unique programs scheduled.")
            st.write("---")
else:
    st.warning("⚠️ Please upload the modified program ratings CSV file first.")
