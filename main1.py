import streamlit as st
import pdfkit
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

st.set_page_config(
    page_title="Building Energy Predictor",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for colors and layout
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .main-title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .main-title span {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(45deg, #FF0000, #FF4500, #FF8C00); /* RED-ORANGE gradient */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .section-header {
            color: red; /* Section headers in red */
            font-size: 22px;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 10px;
            border-bottom: 2px solid red;
            padding-bottom: 4px;
        }
        .footer {
            font-size: 14px;
            text-align: center;
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)

def generate_pdf_report(eui, energy_outcome, peak_load):
    from io import BytesIO
    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, f"EUI (kWh/m².Yr): {eui:.2f}")
    c.drawString(100, 730, f"Energy Outcome: {energy_outcome}")
    c.drawString(100, 710, f"Peak Load (kW): {peak_load:.1f}")

    c.drawString(100, 690, "🔋 This is a test with emoji support (if your PDF viewer supports it).")

    c.save()

    buffer.seek(0)
    return buffer.read()

# Top layout with logo at top-right
col_logo, col_title = st.columns([0.85, 0.15])

with col_logo:
    st.markdown(
        """
        <div class="main-title">
            <span>Building Energy Predictor</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_title:
    st.image("images/EDSlogo.jpg", width=100)

# Divide into 65% and 35% columns
col1, col2 = st.columns([0.65, 0.35])

# ---------------- LEFT COLUMN (Inputs) ----------------
with col1:
    st.markdown('<div class="section-header"> Building Inputs</div>', unsafe_allow_html=True)

    colA, colB, colAA = st.columns(3)
    with colA:
        location = st.selectbox(" Location", [
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
            "Kolkata", "Ahmedabad", "Pune", "Jaisalmer", "Srinagar"
        ])
    with colB:
        building_typology = st.selectbox(" Building Typology", [
            "Office", "Residential", "Hospital", "Retail", "Hotel", "Education"
        ])
    with colAA:
        orient = st.selectbox(" Orientation (degrees)", ["0", "45", "90", "135", "180", "225", "270", "315"])

    colC, colD, colCC, colDD = st.columns(4)
    with colC:
        above_grade_area = st.number_input(" Above Grade Area (m²)", min_value=100, value=1000)
    with colD:
        below_grade_area = st.number_input(" Below Grade Area (m²)", min_value=0, value=0)

    # colCC, colDD = st.columns(2)
    with colCC:
        cond_area = st.number_input(" Conditioned Area (m²)", min_value=100, value=1000)
    with colDD:
        uncond_area = st.number_input(" Unconditioned Area (m²)", min_value=0, value=0)

    # Envelope Characteristics
    st.markdown('<div class="section-header">Envelope Characteristics</div>', unsafe_allow_html=True)

    colE, colF, colG, colH = st.columns(4)
    with colE:
        window_wall_ratio = st.slider(" Window-to-Wall Ratio", 0.0, 1.0, 0.4, 0.01)
    with colF:
        wall_u_value = st.number_input(" Wall U-Value (W/m²·K)", min_value=0.1, value=1.5)
    with colG:
        roof_u_value = st.number_input(" Roof U-Value (W/m²·K)", min_value=0.1, value=1.5)
    with colH:
        window_u_value = st.number_input(" Window U-Value (W/m²·K)", min_value=0.1, value=1.5)

    # Internal Loads
    st.markdown('<div class="section-header"> Internal Loads</div>', unsafe_allow_html=True)

    colI, colJ = st.columns(2)
    with colI:
        lighting_load = st.number_input(" Lighting Load (W/m²)", min_value=0.0, value=10.0)
    with colJ:
        equipment_load = st.number_input(" Equipment Load (W/m²)", min_value=0.0, value=15.0)

    # Predict Button
    st.markdown("<br>", unsafe_allow_html=True)

    predict_button = st.button("🔍 Predict Energy Performance", type="primary")

# ---------------- RIGHT COLUMN (Outputs) ----------------
# Prediction Section
with col2:
    st.markdown('<div class="section-header" style="font-size: 22px; font-weight: bold; color: red; margin-bottom: 20px;">🔎 Predicted Outputs</div>', unsafe_allow_html=True)

    if predict_button:
        eui = 100
        # Mocked for now - you can adjust based on EUI or your logic
        if eui < 100:
            energy_outcome = "Low"
        elif eui < 200:
            energy_outcome = "Medium"
        else:
            energy_outcome = "High"

        peak_load = eui * 0.3  # Placeholder logic, update if you have actual logic for peak load

        st.success("✅ Prediction Complete")

        # Use container to style and align metrics
        with st.container():
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-box">
                    <div class="metric-label">🔋 EUI (kWh/m².Yr)</div>
                    <div class="metric-value">{eui:.2f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">🌍 Energy Outcome</div>
                    <div class="metric-value">{energy_outcome}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">⚡ Peak Load (kW/SQFT)</div>
                    <div class="metric-value">{peak_load:.1f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Download button with PDF report
        pdf_bytes = generate_pdf_report(eui, energy_outcome, peak_load)
        st.download_button(label="📥 Download Report (PDF)", data=pdf_bytes, file_name="energy_performance_report.pdf", mime="application/pdf")

    else:
        st.info("👈 Fill the inputs and click **Predict Energy Performance** to generate predictions.")
# Footer
st.markdown("---")
# Load dataset (replace with your actual file path)
# Footer
st.markdown("---")
st.markdown('<div class="footer">👨‍💻 Developed as part of Machine Learning Energy Modeling Application | © 2025</div>', unsafe_allow_html=True)