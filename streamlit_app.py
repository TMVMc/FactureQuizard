
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Plastic Jewelry Manufacturing Selector", layout="centered")

# Custom CSS for pastel neon vaporwave style
st.markdown(
    """
    <style>
    /* Page background */
    .reportview-container {
        background: linear-gradient(135deg, #ff9a9e, #fad0c4);
        color: #333333;
        font-family: 'Courier New', Courier, monospace;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #a18cd1, #fbc2eb);
    }
    /* Title styling */
    h1 {
        color: #5d3fd3;
        text-align: center;
    }
    h2, h3 {
        color: #333333;
    }
    /* Button styling */
    div.stButton > button {
        background-color: #ff9a9e;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.2);
    }
    /* Input styling */
    .stRadio > div > label {
        font-size: 16px;
        color: #333333;
    }
    .stSelectbox > div > label {
        font-size: 16px;
        color: #333333;
    }
    .stMarkdown {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and introduction
st.title("FactureQuizard")
st.subheader("Plastic Jewelry Manufacturing Process Selector")
st.write("Answer the questions below to determine the best manufacturing process for your jewelry design.")

# Create a form for user input
with st.form(key="manufacturing_form"):
    volume = st.radio("1. What is your expected production volume?", ("Low", "High"))
    detail = st.selectbox("2. How important are intricate details in your design?", ("Low", "Medium", "High"))
    durability = st.radio("3. Is a high-quality finish and durable material important?", ("Yes", "No"))
    budget = st.radio("4. Is your budget limited?", ("Yes", "No"))
    prototyping = st.radio("5. Do you need a fast prototyping process?", ("Yes", "No"))
    recyclable = st.radio("6. Should the final product be recyclable?", ("Yes", "No"))
    hot = st.radio("7. Does the product need to withstand hot environments?", ("Yes", "No"))
    repeatability = st.selectbox("8. How critical is manufacturing repeatability?", ("Low", "Medium", "High"))
    turnaround = st.radio("9. Is quick turnaround (speed of production) very important?", ("Yes", "No"))
    
    submitted = st.form_submit_button("Get Recommendation")

# Process the input and generate recommendation when the form is submitted
if submitted:
    # Initialize scores for each process option
    # Options:
    # - FDM (Fused Deposition Modeling)
    # - SLS (Selective Laser Sintering)
    # - Injection Molding with SLS-Printed Mold (lower cost, quick turnaround)
    # - Injection Molding with Metal-Milled Mold (high repeatability, high volume)
    score_fdm = 0
    score_sls = 0
    score_injection_sls = 0
    score_injection_metal = 0

    # Normalize inputs to lowercase for scoring logic
    vol = volume.lower()
    det = detail.lower()
    dur = durability.lower()
    bud = budget.lower()
    proto = prototyping.lower()
    recyc = recyclable.lower()
    hot_env = hot.lower()
    rep = repeatability.lower()
    turn = turnaround.lower()

    # 1. Production Volume
    if vol == "low":
        score_injection_metal -= 2  # Metal molds are expensive for low volume.
        score_injection_sls -= 1
        score_fdm += 1
        score_sls += 1
    elif vol == "high":
        score_injection_metal += 2  # Ideal for high-volume production.
        score_injection_sls += 1
        score_fdm -= 1
        score_sls += 1

    # 2. Design Intricacy/Detail
    if det == "high":
        score_sls += 2  # SLS captures fine details very well.
        score_injection_metal += 1
        score_injection_sls += 1
        score_fdm -= 1  # FDM may lose some details.
    elif det == "medium":
        score_sls += 1
        score_injection_metal += 1
        score_injection_sls += 1
    elif det == "low":
        score_fdm += 1

    # 3. Finish & Durability
    if dur == "yes":
        score_injection_metal += 2  # Metal-milled molds produce high-quality finishes.
        score_injection_sls += 1
        score_sls += 1
        score_fdm -= 1  # FDM parts may need extra post-processing.
    else:
        score_fdm += 1

    # 4. Budget Constraints
    if bud == "yes":
        score_injection_metal -= 2  # Traditional metal molds are costly.
        score_injection_sls -= 1
        score_fdm += 1
        score_sls += 1
    else:
        score_injection_metal += 1
        score_injection_sls += 1

    # 5. Prototyping Speed
    if proto == "yes":
        score_fdm += 2  # FDM is very fast for prototyping.
        score_sls += 1
        score_injection_sls += 1
        score_injection_metal -= 1  # Metal molds take longer.
    else:
        score_injection_metal += 1
        score_injection_sls += 1

    # 6. Recyclability
    if recyc == "yes":
        score_fdm += 1
        score_injection_metal += 1
        score_injection_sls += 1
        score_sls -= 1  # SLS resins are typically less recyclable.
    else:
        score_sls += 1

    # 7. Hot Environment Resistance
    if hot_env == "yes":
        score_fdm -= 1  # FDM plastics may not hold up well in hot conditions.
    else:
        score_fdm += 1

    # 8. Manufacturing Repeatability
    if rep == "high":
        score_injection_metal += 2  # Metal molds offer high repeatability.
        score_injection_sls += 1
        score_fdm -= 1
        score_sls -= 1
    elif rep == "medium":
        score_injection_metal += 1
        score_injection_sls += 1
    elif rep == "low":
        score_fdm += 1
        score_sls += 1

    # 9. Quick Turnaround
    if turn == "yes":
        score_injection_sls += 2  # SLS-printed molds can be produced quickly.
        score_fdm += 1
        score_sls += 1
        score_injection_metal -= 2  # Metal molds take more time.
    else:
        score_injection_metal += 1

    # Build dictionary of processes and their scores.
    processes = {
        "FDM (Fused Deposition Modeling)": score_fdm,
        "SLS (Selective Laser Sintering)": score_sls,
        "Injection Molding with SLS-Printed Mold": score_injection_sls,
        "Injection Molding with Metal-Milled Mold": score_injection_metal,
    }

    # ----- Invalidation Conditions -----
    if bud == "yes":
        processes["Injection Molding with Metal-Milled Mold"] = float("-inf")
    if recyc == "yes":
        processes["SLS (Selective Laser Sintering)"] = float("-inf")
        processes["Injection Molding with SLS-Printed Mold"] = float("-inf")
    if hot_env == "yes":
        processes["FDM (Fused Deposition Modeling)"] = float("-inf")

    # Determine the best option
    recommended = max(processes, key=processes.get)

    # Display the recommendation
    if processes[recommended] == float("-inf"):
        st.error("Based on your criteria, none of the available processes fully meet your requirements. Please consider revisiting your priorities.")
    else:
        st.success(f"Recommended Process: {recommended}")

    st.subheader("Score Breakdown")
    for process, score in processes.items():
        if score == float("-inf"):
            st.markdown(f"**{process}:** *Disqualified based on your criteria*")
        else:
            st.markdown(f"**{process}:** {score}")
