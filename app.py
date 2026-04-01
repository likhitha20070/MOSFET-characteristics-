import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ PDF FUNCTION ------------------
def generate_pdf(name, reg, dept, obs_data):
    file_name = "experiment_report.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("OP-AMP VIRTUAL LAB REPORT", styles['Title']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Name: {name}", styles['Normal']))
    content.append(Paragraph(f"Reg No: {reg}", styles['Normal']))
    content.append(Paragraph(f"Department: {dept}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Observation Data:", styles['Heading2']))
    for row in obs_data:
        content.append(Paragraph(str(row), styles['Normal']))

    content.append(Spacer(1, 10))
    content.append(Paragraph("Result:", styles['Heading2']))
    content.append(Paragraph("Experiment performed successfully and output verified.", styles['Normal']))

    doc.build(content)
    return file_name


# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Op-Amp Virtual Lab", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔬 Virtual Lab Navigation")
page = st.sidebar.radio("Go to", [
    "Aim & Theory",
    "Apparatus Required",
    "Experiment",
    "Quiz",
    "Feedback"
])

# ------------------ PAGE 1 ------------------
if page == "Aim & Theory":
    st.title("🔬 OP-AMP VIRTUAL LAB")

    st.header("🎯 Aim")
    st.write("""
    To study the working and characteristics of Operational Amplifier circuits 
    such as Inverting Amplifier, Non-Inverting Amplifier, and Comparator.
    """)

    st.header("📖 Theory")
    st.write("""
    An Operational Amplifier (Op-Amp) is a high-gain differential amplifier widely used in analog electronics.

    ### Key Features:
    - High input impedance  
    - Low output impedance  
    - High gain  

    ### Configurations:
    🔹 Inverting Amplifier → Gain = -Rf / Rin  
    🔹 Non-Inverting Amplifier → Gain = 1 + (Rf / Rin)  
    🔹 Comparator → Compares voltages  

    ### Applications:
    Amplification, filtering, oscillators, comparators.
    """)

# ------------------ PAGE 2 ------------------
elif page == "Apparatus Required":
    st.title("🧰 Apparatus Required")
    st.write("""
    - Op-Amp IC (741)  
    - Resistors  
    - Breadboard  
    - Power Supply  
    - Function Generator  
    - CRO  
    - Connecting wires  
    """)

# ------------------ PAGE 3 ------------------
elif page == "Experiment":
    st.title("🧪 Experiment")

    st.subheader("👨‍🎓 Student Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name")
    with col2:
        reg = st.text_input("Register Number")
    with col3:
        dept = st.text_input("Department")

    st.subheader("📋 Observation Table")

    obs_data = []
    for i in range(5):
        col1, col2 = st.columns(2)
        with col1:
            vin = st.number_input(f"Vin {i+1}", key=f"vin{i}")
        with col2:
            vout = st.number_input(f"Vout {i+1}", key=f"vout{i}")
        obs_data.append((vin, vout))

    if st.button("▶ Run Experiment"):
        st.success("✅ Experiment has been run successfully!")

        vin_vals = [x[0] for x in obs_data]
        vout_vals = [x[1] for x in obs_data]

        fig, ax = plt.subplots()
        ax.plot(vin_vals, vout_vals, marker='o')
        ax.set_xlabel("Vin")
        ax.set_ylabel("Vout")
        ax.set_title("Graph")

        st.pyplot(fig)

        st.subheader("📌 Result")
        st.write("The Op-Amp characteristics are verified successfully.")

        pdf = generate_pdf(name, reg, dept, obs_data)

        with open(pdf, "rb") as f:
            st.download_button("⬇ Download Report", f, file_name="report.pdf")

# ------------------ PAGE 4 (FIXED QUIZ) ------------------
elif page == "Quiz":
    st.title("🧠 Quiz")

    questions = [
        {"q": "Op-Amp gain is?", "opt": ["High", "Low"], "ans": "High"},
        {"q": "Inverting gain formula?", "opt": ["-Rf/Rin", "Rf/Rin"], "ans": "-Rf/Rin"},
        {"q": "Non-inverting gain?", "opt": ["1+Rf/Rin", "Rf/Rin"], "ans": "1+Rf/Rin"},
        {"q": "Comparator output?", "opt": ["Digital", "Analog"], "ans": "Digital"},
        {"q": "Op-Amp input type?", "opt": ["Differential", "Single"], "ans": "Differential"},
        {"q": "IC used?", "opt": ["741", "555"], "ans": "741"},
        {"q": "Feedback used?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Output saturation?", "opt": ["Yes", "No"], "ans": "Yes"},
        {"q": "Used for?", "opt": ["Amplifier", "Motor"], "ans": "Amplifier"},
        {"q": "Gain type?", "opt": ["Voltage", "Current"], "ans": "Voltage"}
    ]

    user_answers = []

    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['q']}")

        options = ["Select an option"] + q["opt"]

        ans = st.radio(
            "Choose your answer:",
            options,
            index=0,
            key=f"q{i}"
        )

        user_answers.append(ans)

    if st.button("Submit Quiz"):
        score = 0

        for i, q in enumerate(questions):
            if user_answers[i] == q["ans"]:
                score += 1

        st.success(f"Your Score: {score}/10")

# ------------------ PAGE 5 ------------------
elif page == "Feedback":
    st.title("💬 Feedback")

    st.text_input("1. How was the lab experience?")
    st.text_input("2. Was theory clear?")
    st.text_input("3. Experiment interface feedback?")
    st.text_input("4. Suggestions?")
    st.text_input("5. Overall feedback?")

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")
