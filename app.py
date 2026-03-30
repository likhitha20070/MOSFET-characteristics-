import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ PDF (RESULT ONLY) ------------------
def generate_pdf(Vgs, Vt, k):
    file_name = "mosfet_result.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("MOSFET EXPERIMENT RESULT", styles['Title']))
    content.append(Paragraph(f"Vgs: {Vgs}", styles['Normal']))
    content.append(Paragraph(f"Vt: {Vt}", styles['Normal']))
    content.append(Paragraph(f"k: {k}", styles['Normal']))
    content.append(Paragraph("Result: Characteristics verified successfully.", styles['Normal']))

    doc.build(content)
    return file_name

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="MOSFET Virtual Lab", layout="wide")

# ------------------ UI ------------------
st.sidebar.title("🔬 Virtual MOSFET Lab")
section = st.sidebar.radio("Lab Sections", [
    "Home", "Aim", "Apparatus", "Theory",
    "Circuit Diagram", "Procedure",
    "Experiment", "Observations",
    "Result", "Quiz", "Feedback"
])

# ------------------ HOME ------------------
if section == "Home":
    st.title("🔬 MOSFET Virtual Laboratory")
    st.markdown("""
    Welcome to a **Virtual Lab Experience** 🎯  

    This platform simulates a **real lab record digitally**, including:
    - Theory & Procedure  
    - Experiment Simulation  
    - Observations  
    - Result Generation  
    - Viva Questions  

    👉 Follow sections in order like a real lab.
    """)

# ------------------ AIM ------------------
elif section == "Aim":
    st.header("🎯 Aim")
    st.write("To study the output characteristics of an N-channel MOSFET.")

# ------------------ APPARATUS ------------------
elif section == "Apparatus":
    st.header("🧰 Apparatus Required")
    st.write("""
    - MOSFET  
    - DC Power Supply  
    - Ammeter  
    - Voltmeter  
    - Breadboard  
    - Connecting Wires  
    """)

# ------------------ THEORY ------------------
elif section == "Theory":
    st.header("📖 Theory")
    st.write("""
    MOSFET is a voltage-controlled device widely used in electronics.

    ### Regions:
    - Cutoff  
    - Triode  
    - Saturation  

    ### Equation:
    Id = k(Vgs - Vt)^2
    """)

# ------------------ CIRCUIT ------------------
elif section == "Circuit Diagram":
    st.header("🔌 Circuit Diagram")
    st.info("👉 Add MOSFET circuit image here for better visualization.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7e/MOSFET_N-Channel.svg")

# ------------------ PROCEDURE ------------------
elif section == "Procedure":
    st.header("⚙ Procedure")
    st.write("""
    1. Connect the MOSFET circuit  
    2. Apply gate voltage (Vgs)  
    3. Vary drain voltage (Vds)  
    4. Measure drain current (Id)  
    5. Record readings  
    6. Plot graph  
    """)

# ------------------ EXPERIMENT ------------------
elif section == "Experiment":
    st.header("🧪 Perform Experiment")

    Vgs = st.slider("Gate Voltage (Vgs)", 0.0, 5.0, 2.5)
    Vt = st.slider("Threshold Voltage (Vt)", 0.5, 2.0, 1.0)
    k = st.slider("Constant (k)", 0.1, 2.0, 1.0)

    Vds = np.linspace(0, 5, 100)

    Id = []
    for v in Vds:
        if Vgs <= Vt:
            Id.append(0)
        elif v < (Vgs - Vt):
            Id.append(k * ((Vgs - Vt)*v - (v**2)/2))
        else:
            Id.append(k * (Vgs - Vt)**2)

    Id = np.array(Id)

    fig, ax = plt.subplots()
    ax.plot(Vds, Id)
    ax.set_xlabel("Vds")
    ax.set_ylabel("Id")
    ax.set_title("Output Characteristics")

    st.pyplot(fig)

    st.session_state["data"] = (Vgs, Vt, k)

# ------------------ OBSERVATIONS ------------------
elif section == "Observations":
    st.header("📋 Observations")

    if "data" in st.session_state:
        Vgs, Vt, k = st.session_state["data"]
        st.write(f"Vgs: {Vgs}")
        st.write(f"Vt: {Vt}")
        st.write(f"k: {k}")
    else:
        st.warning("⚠ Perform experiment first")

# ------------------ RESULT ------------------
elif section == "Result":
    st.header("📌 Result")

    if "data" in st.session_state:
        Vgs, Vt, k = st.session_state["data"]

        st.success("MOSFET characteristics verified successfully.")

        if st.button("📄 Download Result PDF"):
            pdf = generate_pdf(Vgs, Vt, k)
            with open(pdf, "rb") as f:
                st.download_button("⬇ Download", f, file_name="result.pdf")
    else:
        st.warning("⚠ Perform experiment first")

# ------------------ QUIZ ------------------
elif section == "Quiz":
    st.header("🧠 Viva Questions")

    questions = [
        {"q": "MOSFET is controlled by?", "opt": ["Voltage", "Current"], "ans": "Voltage"},
        {"q": "Region for amplification?", "opt": ["Saturation", "Cutoff"], "ans": "Saturation"},
        {"q": "Vt stands for?", "opt": ["Threshold voltage", "Test voltage"], "ans": "Threshold voltage"},
        {"q": "Drain current symbol?", "opt": ["Id", "Ig"], "ans": "Id"},
        {"q": "MOSFET type?", "opt": ["N-channel", "P-channel", "Both"], "ans": "Both"},
        {"q": "Used as switch?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Gate controls?", "opt": ["Current", "Voltage"], "ans": "Voltage"},
        {"q": "Cutoff current?", "opt": ["Zero", "High"], "ans": "Zero"},
        {"q": "Device type?", "opt": ["Voltage", "Current"], "ans": "Voltage"},
        {"q": "Equation uses?", "opt": ["Vgs", "Vds"], "ans": "Vgs"}
    ]

    score = 0

    for i, q in enumerate(questions):
        ans = st.radio(q["q"], q["opt"], key=i)
        if ans == q["ans"]:
            score += 1

    if st.button("Submit Viva"):
        st.success(f"Score: {score}/10")

# ------------------ FEEDBACK ------------------
elif section == "Feedback":
    st.header("💬 Feedback")

    st.slider("Lab Experience", 1, 5)
    st.slider("Clarity", 1, 5)
    st.slider("UI", 1, 5)
    st.slider("Understanding", 1, 5)
    st.slider("Overall", 1, 5)

    if st.button("Submit"):
        st.success("Thanks for your feedback!")
