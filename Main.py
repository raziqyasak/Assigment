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
# 📂 Load Dataset
# -----------------------------------
st.title("🧩 Genetic Algorithm Scheduler – Multiple Trials (GitHub Data)")

file_path = "program_ratings (1).csv"
data = pd.read_csv(file_path)
st.success(f"✅ Dataset loaded successfully from: {file_path}")

# -----------------------------------
# 🔍 Detect Program Column Automatically
# -----------------------------------
possible_cols = [col for col in data.columns if "program" in col.lower()]
if possible_cols:
    program_col = possible_cols[0]
    st.info(f"Automatically detected Program column: **{program_col}**")
else:
    st.error("❌ Could not detect a 'Program' column in the dataset.")
    st.stop()

# -----------------------------------
# ⚙️ Parameter Settings for 3 Trials
# -----------------------------------
st.subheader("⚙️ Set Parameters for Each Trial")

# --- Trial 1 (Blue) ---
st.markdown(
    """
    <div style="background-color:#e3f2fd; padding:15px; border-radius:10px; margin-bottom:10px;">
    <h4 style="color:#1565c0;">Trial 1 Parameters</h4>
    """,
    unsafe_allow_html=True,
)
co_r1 = st.slider("Trial 1 – Crossover Rate (CO_R)", 0.0, 0.95, 0.8, 0.01)
mut_r1 = st.slider("Trial 1 – Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, 0.01)
st.markdown("</div>", unsafe_allow_html=True)

# --- Trial 2 (Green) ---
st.markdown(
    """
    <div style="background-color:#e8f5e9; padding:15px; border-radius:10px; margin-bottom:10px;">
    <h4 style="color:#2e7d32;">Trial 2 Parameters</h4>
    """,
    unsafe_allow_html=True,
)
co_r2 = st.slider("Trial 2 – Crossover Rate (CO_R)", 0.0, 0.95, 0.6, 0.01)
mut_r2 = st.slider("Trial 2 – Mutation Rate (MUT_R)", 0.01, 0.05, 0.03, 0.01)
st.markdown("</div>", unsafe_allow_html=True)

# --- Trial 3 (Orange) ---
st.markdown(
    """
    <div style="background-color:#fff3e0; padding:15px; border-radius:10px; margin-bottom:10px;">
    <h4 style="color:#ef6c00;">Trial 3 Parameters</h4>
    """,
    unsafe_allow_html=True,
)
co_r3 = st.slider("Trial 3 – Crossover Rate (CO_R)", 0.0, 0.95, 0.4, 0.01)
mut_r3 = st.slider("Trial 3 – Mutation Rate (MUT_R)", 0.01, 0.05, 0.04, 0.01)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# ▶️ Run All Trials
# -----------------------------------
if st.button("🚀 Run All Trials"):
    st.info("Running all 3 genetic algorithm trials...")

    trials = [
        ("Trial 1", co_r1, mut_r1),
        ("Trial 2", co_r2, mut_r2),
        ("Trial 3", co_r3, mut_r3)
    ]

    for name, co_r, mut_r in trials:
        st.subheader(f"{name}")
        st.write(f"**Parameters:** CO_R = {co_r}, MUT_R = {mut_r}")

        # Run GA
        schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data, program_col)
        st.dataframe(schedule_df, use_container_width=True)

        # --- Summary Info (Added Rating) ---
        unique_programs = schedule_df['Program'].nunique()
        avg_rating = round(schedule_df['Fitness Score'].mean(), 2)

        st.write(f"**Summary:** {unique_programs} unique programs scheduled.")
        st.write(f"**Average Rating:** ⭐ {avg_rating}")
        st.write("---")
