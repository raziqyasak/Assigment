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
    # Detect program column automatically
    possible_program_cols = ["Program", "Type of Program", "Program Name", "Programme"]
    program_col = None
    for col in data.columns:
        if any(name.lower() in col.lower() for name in possible_program_cols):
            program_col = col
            break

    if program_col is None:
        st.error("❌ Could not find a 'Program' column in your dataset.")
        st.stop()

    # Detect columns with 'Modified Hour'
    hour_cols = [col for col in data.columns if "Modified Hour" in col]

    if not hour_cols:
        st.error("❌ No 'Modified Hour' columns found in your dataset.")
        st.stop()

    schedule = []

    for hour in hour_cols:
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
st.title("🧬 Genetic Algorithm Scheduler – Multiple Trials (GitHub Dataset)")

st.write("""
You can provide the **GitHub raw file URL** of your dataset (CSV format), 
or upload it manually if it's not online yet.
""")

# Example GitHub URL (you can edit this!)
default_github_url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/program_ratings_modified.csv"

# Input for GitHub path
github_url = st.text_input(
    "Enter the GitHub RAW file URL of your dataset",
    value=default_github_url
)

data = None

# Try to load dataset from GitHub
if github_url and github_url.startswith("http"):
    try:
        response = requests.get(github_url)
        if response.status_code == 200:
            data = pd.read_csv(io.StringIO(response.text))
            st.success("✅ Dataset successfully loaded from GitHub!")
        else:
            st.warning("⚠️ Unable to load from GitHub. Check the URL or repository access.")
    except Exception as e:
        st.error(f"❌ Error loading from GitHub: {e}")

# If GitHub loading fails, allow manual upload
if data is None:
    uploaded_file = st.file_uploader("📂 Or upload your modified program ratings CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("✅ Dataset successfully uploaded!")

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

# Run trials only if data is loaded
if data is not None:
    if st.button("🚀 Run All Trials"):
        st.info("Running all 3 genetic algorithm trials...")

        st.write("### 🧾 Dataset Columns:")
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
    st.warning("⚠️ No dataset found. Please check your GitHub link or upload a CSV.")
