import streamlit as st

# 🎯 Title
st.title("Genetic Algorithm Parameter Input")

st.write("""
Use the sliders below to adjust the **Crossover Rate (CO_R)** and **Mutation Rate (MUT_R)** 
for your genetic algorithm.
""")

# 🧬 Input for Crossover Rate (CO_R)
co_r = st.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,
    step=0.01,
    help="Adjust the crossover rate (range: 0.0 to 0.95)"
)

# 🧪 Input for Mutation Rate (MUT_R)
mut_r = st.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.02,
    step=0.01,
    help="Adjust the mutation rate (range: 0.01 to 0.05)"
)

# 🧾 Display selected parameters
st.subheader("Selected Parameters:")
st.write(f"**Crossover Rate (CO_R):** {co_r}")
st.write(f"**Mutation Rate (MUT_R):** {mut_r}")

# Optional: Use these values in the algorithm
if st.button("Run Genetic Algorithm"):
    st.success(f"Genetic Algorithm initialized with CO_R={co_r} and MUT_R={mut_r}")
