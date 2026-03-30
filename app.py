import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ FUNCTION (TOP ONLY) ------------------
def generate_pdf(Vgs, Vt, k):
    file_name = "mosfet_report.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("MOSFET Experiment Report", styles['Title']))
    content.append(Paragraph(f"Gate Voltage (Vgs): {Vgs}", styles['Normal']))
    content.append(Paragraph(f"Threshold Voltage (Vt): {Vt}", styles['Normal']))
    content.append(Paragraph(f"Constant (k): {k}", styles['Normal']))

    doc.build(content)
    return file_name


# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="MOSFET Virtual Lab", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔬 MOSFET Lab")
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Aim & Theory", "Experiment", "Quiz", "Feedback"]
)

# ------------------ DASHBOARD ------------------
if page == "Dashboard":
    st.title("🔬 MOSFET Virtual Laboratory")
    st.write("Welcome! Use the sidebar to explore the lab.")

# ------------------ AIM & THEORY ------------------
elif page == "Aim & Theory":
    st.title("📘 Aim & Theory")

    st.header("🎯 Aim")
    st.write("To study MOSFET characteristics.")

    st.header("📖 Theory")
    st.write("MOSFET is a voltage-controlled device.")

# ------------------ EXPERIMENT ------------------
elif page == "Experiment":
    st.title("🧪 MOSFET Experiment")

    st.sidebar.header("⚙ Input Parameters")

    Vgs = st.sidebar.slider("Gate Voltage (Vgs)", 0.0, 5.0, 2.5)
    Vt = st.sidebar.slider("Threshold Voltage (Vt)", 0.5, 2.0, 1.0)
    k = st.sidebar.slider("Constant (k)", 0.1, 2.0, 1.0)

    Vds = np.linspace(0, 5, 100)

    Id = []
    for v in Vds:
        if Vgs <= Vt:
            Id.append(0)
        elif v < (Vgs - Vt):
            Id.append(k * ((Vgs - Vt) * v - (v**2) / 2))
        else:
            Id.append(k * (Vgs - Vt) ** 2)

    Id = np.array(Id)

    st.subheader("📊 Output Characteristics")

    fig, ax = plt.subplots()
    ax.plot(Vds, Id)
    ax.set_xlabel("Vds")
    ax.set_ylabel("Id")

    st.pyplot(fig)

    st.subheader("📌 Results")
    st.write(f"Vgs = {Vgs}, Vt = {Vt}, k = {k}")

    # ✅ PDF DOWNLOAD ONLY HERE
    if st.button("📄 Generate Report"):
        pdf_file = generate_pdf(Vgs, Vt, k)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                data=f,
                file_name="mosfet_report.pdf"
            )

# ------------------ QUIZ ------------------
elif page == "Quiz":
    st.title("🧠 Quiz")

    questions = [
        {"q": "MOSFET is a ___ controlled device?", "opt": ["Current", "Voltage"], "ans": "Voltage"},
        {"q": "Vt means?", "opt": ["Threshold voltage", "Test voltage"], "ans": "Threshold voltage"}
    ]

    score = 0

    for i, q in enumerate(questions):
        ans = st.radio(q["q"], q["opt"], key=i)
        if ans == q["ans"]:
            score += 1

    if st.button("Submit"):
        st.success(f"Score: {score}/{len(questions)}")

# ------------------ FEEDBACK ------------------
elif page == "Feedback":
    st.title("💬 Feedback")

    st.slider("UI", 1, 5)
    st.slider("Clarity", 1, 5)
    st.slider("Usefulness", 1, 5)
    st.slider("Ease", 1, 5)
    st.slider("Overall", 1, 5)

    if st.button("Submit"):
        st.success("Thanks for feedback!")
