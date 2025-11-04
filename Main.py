import streamlit as st
import pandas as pd
import numpy as np

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
        data["Score"] = data[hour] + np.random.uniform(-mut_r, mut_r, len(data))
        best_row = data.loc[data["Score"].idxmax()]
        schedule.append({
            "Hour": hour.replace("Modified ", ""),
            "Program": best_row[program_col],
            "Fitness Score": round(best_row[hour], 2)
        })

    return pd.DataFrame(schedule)


# -----------------------------------
# 🌟 App Layout & Styling
# -----------------------------------
st.set_page_config(page_title="Genetic Algorithm Scheduler", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f9fbfd;
        padding: 20px;
        border-radius: 10px;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .title {
        text-align: center;
        color: #1e3a8a;
        font-weight: bold;
        font-size: 2rem;
    }
    .subheader {
        font-weight: 600;
        color: #374151;
        margin-top: 10px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .trial-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# 🧾 Load Dataset
# -----------------------------------
st.markdown("<p class='title'>🧬 Genetic Algorithm Scheduler – Multi-Trial Dashboard</p>", unsafe_allow_html=True)

file_path = "program_ratings (1).csv"
try:
    data = pd.read_csv(file_path)
    st.success(f"✅ Dataset loaded successfully from: `{file_path}`")
except Exception as e:
    st.error(f"❌ Failed to load dataset: {e}")
    st.stop()

# Auto-detect Program column
possible_cols = [col for col in data.columns if "program" in col.lower()]
if possible_cols:
    program_col = possible_cols[0]
    st.info(f"🧩 Automatically detected Program column: **{program_col}**")
else:
    st.error("❌ Could not detect a 'Program' column in the dataset.")
    st.stop()


# -----------------------------------
# ⚙️ Parameter Settings Section
# -----------------------------------
st.markdown("<h3 class='subheader'>⚙️ Configure Genetic Algorithm Parameters</h3>", unsafe_allow_html=True)
st.write("Adjust crossover and mutation rates for each trial below:")

col1, col2, col3 = st.columns(3)

# --- Trial 1 (Blue) ---
with col1:
    st.markdown("<div class='card' style='border-left:6px solid #1e88e5;'>", unsafe_allow_html=True)
    st.markdown("<p class='trial-title' style='color:#1e88e5;'>Trial 1 Parameters</p>", unsafe_allow_html=True)
    co_r1 = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8, 0.01, key="co1")
    mut_r1 = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, 0.01, key="mut1")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Trial 2 (Green) ---
with col2:
    st.markdown("<div class='card' style='border-left:6px solid #43a047;'>", unsafe_allow_html=True)
    st.markdown("<p class='trial-title' style='color:#43a047;'>Trial 2 Parameters</p>", unsafe_allow_html=True)
    co_r2 = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.6, 0.01, key="co2")
    mut_r2 = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.03, 0.01, key="mut2")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Trial 3 (Orange) ---
with col3:
    st.markdown("<div class='card' style='border-left:6px solid #fb8c00;'>", unsafe_allow_html=True)
    st.markdown("<p class='trial-title' style='color:#fb8c00;'>Trial 3 Parameters</p>", unsafe_allow_html=True)
    co_r3 = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.4, 0.01, key="co3")
    mut_r3 = st.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.04, 0.01, key="mut3")
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------
# ▶️ Run All Trials
# -----------------------------------
st.markdown("---")
if st.button("🚀 Run All Genetic Algorithm Trials", use_container_width=True, type="primary"):
    st.info("Running all 3 trials, please wait...")

    trials = [
        ("Trial 1", co_r1, mut_r1, "#1e88e5"),
        ("Trial 2", co_r2, mut_r2, "#43a047"),
        ("Trial 3", co_r3, mut_r3, "#fb8c00")
    ]

    for name, co_r, mut_r, color in trials:
        st.markdown(f"<h4 style='color:{color}; font-weight:700;'>{name}</h4>", unsafe_allow_html=True)
        st.write(f"**Parameters:** CO_R = `{co_r}`, MUT_R = `{mut_r}`")

        schedule_df = run_genetic_algorithm_with_data(co_r, mut_r, data, program_col)
        st.dataframe(schedule_df, use_container_width=True)
        st.success(f"✅ {schedule_df['Program'].nunique()} unique programs scheduled in {name}.")
        st.markdown("---")
