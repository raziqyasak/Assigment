import streamlit as st
import pandas as pd
import numpy as np
import requests
import io

# -----------------------------------
# 🧬 Genetic Algorithm Simulation
# -----------------------------------
def run_genetic_algorithm_with_data(co_r, mut_r, data):
    """
    Simulate a GA that selects the best program for each hour
    based on modified ratings and random variation.
    """
    # --- Detect program column automatically ---
    possible_program_cols = ["program", "type of program", "programme", "program name"]
    program_col = None

    for col in data.columns:
        if any(keyword in col.lower() for keyword in possible_program_cols):
            program_col = col
            break

    if program_col is None:
        st.error("❌ Could not automatically detect the program column. Please ensure your dataset contains a column like 'Program' or 'Type of Program'.")
        st.stop()

    # --- Detect hour columns ---
    hour_cols = [col for col in data.columns if "modified hour" in col.lower()]
    if not hour_cols:
        st.error("❌ No 'Modified Hour' columns found in the dataset.")
        st.stop()

    schedule = []
    for hour in hour_cols:
        # Simulate random mutation and selection
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
st.title("🧬 Genetic Algorithm Scheduler – Multiple Trials")

st.write("""
You can provide the **GitHub raw file URL** or upload your **Program Ratings Dataset (CSV/XLSX)**.  
The system will automatically detect your program column and schedule columns.
""")

# Example GitHub URL (you can replace this)
default_github_url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/program_ratings_modified.csv"

# GitHub URL input
github_url = st.text_input("Enter GitHub RAW file URL", value=default_github_url)

data = None

# --- Load from GitHub URL ---
if github_url and github_url.startswith("http"):
    try:
        response = requests.get(github_url)
        if response.status_code == 200:
            if github_url.endswith(".csv"):
                data = pd.read_csv(io.StringIO(response.text))
            elif github_url.endswith((".xls", ".xlsx")):
                data = pd.read_excel(io.BytesIO(response.content))
            else:
                st.warning("⚠️ Unsupported file format. Please use CSV or Excel.")
            if data is not None:
                st.success("✅ Dataset successfully loaded from GitHub!")
        else:
            st.warning("⚠️ Could not load from GitHub. Please check the URL.")
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")

# --- Fallback: Manual Upload ---
if data is None:
    uploaded_file = st.file_uploader("📂 Or upload your dataset", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            data = pd.read_excel(uploaded_file)
        st.success("✅ Dataset successfully uploaded!")

# --- Parameter Inputs ---
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

# --- Run the Algorithm ---
if data is not None:
    if st.button("🚀 Run All Trials"):
        st.info("Running all 3 genetic algorithm trials...")
        st.write("### 📊 Dataset Columns:")
        st.write(data.columns.tolist())

        trials = [
            ("Trial 1", co_r1, mut_r1),
            ("Trial 2", co_r2, mut_r2),
            ("Trial 3", co_r3, mut_r3)
        ]

        for name, co_r, mut_r in trials:
            st.subheader(f"🧬 {name}")
            st.write(f"**Parameters:** CO_R = `{co_r}`, MUT_R = `{mut_r}`")

            schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data)
            st.dataframe(schedule_df, use_container_width=True)
            st.write(f"**Summary:** {schedule_df['Program'].nunique()} unique programs scheduled.")
            st.write("---")
else:
    st.warning("⚠️ Please upload or link a valid dataset first.")
