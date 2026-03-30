import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ PDF FUNCTION ------------------
def generate_pdf(exp_type, result):
    file_name = "opamp_result.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("OP-AMP EXPERIMENT RESULT", styles['Title']))
    content.append(Paragraph(f"Experiment: {exp_type}", styles['Normal']))
    content.append(Paragraph(f"Result: {result}", styles['Normal']))

    doc.build(content)
    return file_name

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Op-Amp Virtual Lab", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔬 Op-Amp Virtual Lab")
section = st.sidebar.radio("Sections", [
    "Home", "Aim", "Apparatus", "Theory",
    "Procedure", "Experiment", "Result",
    "Quiz", "Feedback"
])

# ------------------ HOME ------------------
if section == "Home":
    st.title("🔬 Operational Amplifier Virtual Lab")

    st.markdown("""
    A complete **virtual lab experience** for studying Op-Amp circuits.

    ### Experiments Included:
    - Inverting Amplifier  
    - Non-Inverting Amplifier  
    - Comparator  

    👉 Follow sections step-by-step like a real lab.
    """)

# ------------------ AIM ------------------
elif section == "Aim":
    st.header("🎯 Aim")
    st.write("To study various Op-Amp configurations and their behavior.")

# ------------------ APPARATUS ------------------
elif section == "Apparatus":
    st.header("🧰 Apparatus")
    st.write("""
    - Operational Amplifier (IC 741)  
    - Resistors  
    - Power Supply  
    - Function Generator  
    - CRO  
    """)

# ------------------ THEORY ------------------
elif section == "Theory":
    st.header("📖 Theory")
    st.write("""
    An Operational Amplifier (Op-Amp) is a high-gain voltage amplifier.

    ### Key Configurations:
    - Inverting Amplifier  
    - Non-Inverting Amplifier  
    - Comparator  

    ### Gain Formula:
    Inverting: Gain = -Rf / Rin  
    Non-Inverting: Gain = 1 + (Rf / Rin)
    """)

# ------------------ PROCEDURE ------------------
elif section == "Procedure":
    st.header("⚙ Procedure")
    st.write("""
    1. Connect the Op-Amp circuit  
    2. Apply input signal  
    3. Observe output waveform  
    4. Calculate gain  
    5. Verify results  
    """)

# ------------------ EXPERIMENT ------------------
elif section == "Experiment":
    st.header("🧪 Perform Experiment")

    exp_type = st.selectbox("Select Experiment", [
        "Inverting Amplifier",
        "Non-Inverting Amplifier",
        "Comparator"
    ])

    result_text = ""

    # -------- Inverting --------
    if exp_type == "Inverting Amplifier":
        Rin = st.slider("Input Resistance (Rin)", 1, 100, 10)
        Rf = st.slider("Feedback Resistance (Rf)", 1, 100, 50)
        Vin = st.slider("Input Voltage", 0.1, 5.0, 1.0)

        gain = -Rf / Rin
        Vout = gain * Vin

        result_text = f"Gain = {gain}, Output Voltage = {Vout}"
        st.write(result_text)

    # -------- Non-Inverting --------
    elif exp_type == "Non-Inverting Amplifier":
        Rin = st.slider("Rin", 1, 100, 10)
        Rf = st.slider("Rf", 1, 100, 50)
        Vin = st.slider("Input Voltage", 0.1, 5.0, 1.0)

        gain = 1 + (Rf / Rin)
        Vout = gain * Vin

        result_text = f"Gain = {gain}, Output Voltage = {Vout}"
        st.write(result_text)

    # -------- Comparator --------
    elif exp_type == "Comparator":
        Vin = st.slider("Input Voltage", -5.0, 5.0, 1.0)
        Vref = st.slider("Reference Voltage", -5.0, 5.0, 0.0)

        Vout = 5 if Vin > Vref else -5

        result_text = f"Output Voltage = {Vout}"
        st.write(result_text)

    # Graph
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Sample Output Waveform")

    st.pyplot(fig)

    st.session_state["result"] = (exp_type, result_text)

# ------------------ RESULT ------------------
elif section == "Result":
    st.header("📌 Result")

    if "result" in st.session_state:
        exp_type, result_text = st.session_state["result"]

        st.success(result_text)

        if st.button("📄 Download PDF"):
            pdf = generate_pdf(exp_type, result_text)
            with open(pdf, "rb") as f:
                st.download_button("⬇ Download", f, file_name="opamp_result.pdf")
    else:
        st.warning("⚠ Perform experiment first")

# ------------------ QUIZ ------------------
elif section == "Quiz":
    st.header("🧠 Viva Questions")

    questions = [
        {"q": "Op-Amp gain is?", "opt": ["High", "Low"], "ans": "High"},
        {"q": "Inverting gain formula?", "opt": ["-Rf/Rin", "Rf/Rin"], "ans": "-Rf/Rin"},
        {"q": "Non-inverting gain?", "opt": ["1+Rf/Rin", "Rf/Rin"], "ans": "1+Rf/Rin"},
        {"q": "Comparator output?", "opt": ["Digital", "Analog"], "ans": "Digital"},
        {"q": "Op-Amp input?", "opt": ["Differential", "Single"], "ans": "Differential"},
        {"q": "IC used?", "opt": ["741", "555"], "ans": "741"},
        {"q": "Gain type?", "opt": ["Voltage", "Current"], "ans": "Voltage"},
        {"q": "Feedback used?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Output saturation?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Used in?", "opt": ["Amplifier", "Motor"], "ans": "Amplifier"}
    ]

    score = 0

    for i, q in enumerate(questions):
        ans = st.radio(q["q"], q["opt"], key=i)
        if ans == q["ans"]:
            score += 1

    if st.button("Submit"):
        st.success(f"Score: {score}/10")

# ------------------ FEEDBACK ------------------
elif section == "Feedback":
    st.header("💬 Feedback")

    st.slider("Understanding", 1, 5)
    st.slider("UI", 1, 5)
    st.slider("Simulation", 1, 5)
    st.slider("Clarity", 1, 5)
    st.slider("Overall", 1, 5)

    if st.button("Submit"):
        st.success("Thanks for your feedback!")
