import streamlit as st
import pandas as pd
import numpy as np
import os

# -----------------------------------
# 🧬 Genetic Algorithm Simulation
# -----------------------------------
def run_genetic_algorithm_with_data(co_r, mut_r, data):
    """
    Simulate a GA that selects the best program for each hour
    based on modified ratings and random variation.
    """

    # 🔍 Automatically detect the column containing program names
    program_col = None
    for col in data.columns:
        if "program" in col.lower():
            program_col = col
            break

    if program_col is None:
        raise KeyError("No column found containing program names. Please ensure one column includes 'Program' in its name.")

    # 🔍 Identify all modified hour columns
    hour_cols = [col for col in data.columns if "modified hour" in col.lower()]
    if not hour_cols:
        raise KeyError("No columns found with 'Modified Hour' in their names. Please verify your dataset.")

    schedule = []

    for hour in hour_cols:
        # Add random variation to simulate mutation
        data["Score"] = data[hour] + np.random.uniform(-mut_r, mut_r, len(data))
        best_idx = data["Score"].idxmax()
        best_program = data.loc[best_idx, program_col]
        best_score = data.loc[best_idx, hour]

        schedule.append({
            "Hour": hour.replace("Modified ", ""),
            "Program": best_program,
            "Fitness Score": round(best_score, 2)
        })

    return pd.DataFrame(schedule)


# -----------------------------------
# 🎛️ Streamlit Interface
# -----------------------------------
st.title("🧩 Genetic Algorithm Scheduler – Multiple Trials")

st.write("""
Upload your **Program Ratings Dataset (CSV)** or auto-load the default file in the folder,
and run the **Genetic Algorithm** three times with different parameters.
""")

# Try to auto-load local dataset if exists
default_path = "program_ratings_modified.csv"
data = None

if os.path.exists(default_path):
    st.success(f"✅ Found local dataset: {default_path}")
    data = pd.read_csv(default_path)
else:
    uploaded_file = st.file_uploader("📤 Upload the modified program ratings CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("✅ Dataset successfully uploaded!")

# Display dataset info for debugging
if data is not None:
    st.write("### 📋 Dataset Columns:")
    st.write(list(data.columns))

# -----------------------------------
# ⚙️ Parameter Input for 3 Trials
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
# ▶️ Run GA Trials
# -----------------------------------
if data is not None:
    if st.button("🚀 Run All Trials"):
        st.info("Running all 3 genetic algorithm trials...")

        trials = [
            ("Trial 1", co_r1, mut_r1),
            ("Trial 2", co_r2, mut_r2),
            ("Trial 3", co_r3, mut_r3)
        ]

        for name, co_r, mut_r in trials:
            st.subheader(f"🧬 {name}")
            st.write(f"**Parameters:** CO_R = {co_r}, MUT_R = {mut_r}")

            try:
                schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data)
                st.dataframe(schedule_df, use_container_width=True)
                st.write(f"**Summary:** {schedule_df['Program'].nunique()} unique programs scheduled.")
            except KeyError as e:
                st.error(f"❌ Error in {name}: {e}")
            st.write("---")
else:
    st.warning("⚠️ No dataset found. Please upload or place 'program_ratings_modified.csv' in the same folder.")
