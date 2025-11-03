import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO

# -----------------------------------
# 🧬 Genetic Algorithm Simulation
# -----------------------------------
def run_genetic_algorithm_with_data(co_r, mut_r, data, program_col):
    """
    Simulate a GA that selects the best program for each hour
    based on modified ratings and random variation.
    """
    hour_cols = [col for col in data.columns if "Modified Hour" in col or "Hour" in col]
    schedule = []

    for hour in hour_cols:
        # Add random variation based on mutation rate
        data["Score"] = data[hour] + np.random.uniform(-mut_r, mut_r, len(data))
        best_row = data.loc[data["Score"].idxmax()]

        schedule.append({
            "Hour": hour.replace("Modified ", ""),
            "Program": best_row[program_col],
            "Fitness Score": round(best_row[hour], 2)
        })

    return pd.DataFrame(schedule)


# -----------------------------------
# 📂 Load Dataset from GitHub Path
# -----------------------------------
st.title("📺 Genetic Algorithm Scheduler – Multiple Trials (GitHub Data)")

st.write("""
This app automatically loads a dataset from GitHub and runs the **Genetic Algorithm (GA)**
three times using different Crossover (CO_R) and Mutation (MUT_R) rates.
""")

# Change this URL to your actual GitHub raw file link
github_csv_url = "https://raw.githubusercontent.com/USERNAME/REPO/main/program_ratings_modified.csv"

try:
    response = requests.get(github_csv_url)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text))
    st.success("✅ Dataset successfully loaded from GitHub!")
except Exception as e:
    st.error(f"❌ Failed to load dataset from GitHub. Please check the file URL.\n\nError: {e}")
    st.stop()

# -----------------------------------
# 🧭 Detect Program Column Automatically
# -----------------------------------
possible_cols = [col for col in data.columns if "program" in col.lower()]
if possible_cols:
    program_col = possible_cols[0]
    st.info(f"✅ Automatically detected Program column: **{program_col}**")
else:
    st.error("❌ Could not detect a 'Program' column in the dataset.")
    st.stop()

# -----------------------------------
# ⚙️ Parameter Settings for 3 Trials
# -----------------------------------
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

# -----------------------------------
# ▶️ Run All Trials
# -----------------------------------
if st.button("Run All Trials"):
    st.info("🧬 Running all 3 genetic algorithm trials...")

    trials = [
        ("Trial 1", co_r1, mut_r1),
        ("Trial 2", co_r2, mut_r2),
        ("Trial 3", co_r3, mut_r3)
    ]

    for name, co_r, mut_r in trials:
        st.subheader(f"🧪 {name}")
        st.write(f"**Parameters:** CO_R = {co_r}, MUT_R = {mut_r}")

        schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data, program_col)
        st.dataframe(schedule_df, use_container_width=True)
        st.write(f"**Summary:** {schedule_df['Program'].nunique()} unique programs scheduled.")
        st.write("---")
