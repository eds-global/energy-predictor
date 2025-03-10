import streamlit as st
import pandas as pd
import pickle
import numpy as np
import pdfkit
import bz2
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Building Energy Predictor",
    page_icon="🏙️", layout="wide", initial_sidebar_state="collapsed")

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
            margin-bottom: 10px;
            font-weight: bold;
        }
        .main-title span {
            font-size: 38px;
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
        <style>
            .main-title {
                font-size: 0px;  /* Adjust the size as needed */
                font-weight: bold;
            }
        </style>
        <div class="main-title">
            <span>Building Energy Predictor</span>
        </div>""", unsafe_allow_html=True)
with col_title:
    st.image("images/EDSlogo.jpg", width=100)

# Divide into 65% and 35% columns
colA, colB = st.columns([0.65, 0.35])

# ---------------- LEFT COLUMN (Inputs) ----------------
with colA:
    st.markdown('<div class="section-header"> Building Inputs</div>', unsafe_allow_html=True)

    # --- FIRST ROW: Location, Typology, Orientation ---
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        location_climate_map = {
            "Mumbai": "Warm & Humid", "Delhi": "Composite", "Bangalore": "Temperate",
            "Hyderabad": "Composite", "Chennai": "Warm & Humid", "Kolkata": "Warm & Humid",
            "Ahmedabad": "Hot & Dry", "Pune": "Composite", "Jaisalmer": "Hot & Dry",
            "Srinagar": "Cold"
        }
        location = st.selectbox("Location", list(location_climate_map.keys()))
        climate = location_climate_map[location]
        st.markdown(f"**Climate:** {climate}", unsafe_allow_html=True)

    with col2:
        building_typology = st.selectbox(
            "Building Typology",
            ["Business", "Residential", "Hospital", "Retail", "Hotel", "Education"],
            index=0
        )

    with col3:
        orient = st.selectbox("Orientation (degrees)", ["0", "45", "90", "135", "180", "225", "270", "315"])

    st.divider()

    # --- SECOND ROW: Built-Up Areas ---
    col4, col5, col6 = st.columns([1, 1, 1])

    with col4:
        total_builtup_area = st.number_input("Total Built-Up Area (m²)", min_value=100.0, value=1000.0, format="%.0f")

    with col5:
        above_grade_percentage = st.slider("Above Grade Area (%)", min_value=0, max_value=100, value=50)
        above_grade_area = (above_grade_percentage / 100) * total_builtup_area
        below_grade_area = total_builtup_area - above_grade_area

    with col6:
        st.markdown(f"**Above Grade Area (m²):** {above_grade_area:.0f}", unsafe_allow_html=True)  
        st.markdown(f"**Below Grade Area (m²):** {below_grade_area:.0f}", unsafe_allow_html=True)

    st.divider()

    # --- THIRD ROW: Conditioned & Roof Areas ---
    col7, col8, col9 = st.columns([1, 1, 1])
    with col7:
        wall_tot_ag_area = st.number_input("Total Above-Grade Exterior Wall Area (m²)", min_value=100.0, value=1000.0, format="%.0f")
    with col8:
        roof_area = st.number_input("Roof Area (m²)", min_value=100.0, value=1000.0, format="%.0f")
    with col9:
        cond_area_percentage = st.slider("Conditioned Area (%)", min_value=0, max_value=100, value=50)
        cond_area = (cond_area_percentage / 100) * above_grade_area
        uncond_area = total_builtup_area - cond_area
        st.markdown(f"**Conditioned Area (m²):** {cond_area:.0f}", unsafe_allow_html=True)  
        st.markdown(f"**Unconditioned Area (m²):** {uncond_area:.0f}", unsafe_allow_html=True)

    # Envelope Characteristics
    st.markdown('<div class="section-header">Envelope Characteristics</div>', unsafe_allow_html=True)

    colE, colF, colG = st.columns(3)
    with colE:
        window_wall_ratio = st.slider(" Window-to-Wall Ratio", 0.0, 1.0, 0.4, 0.01)
    with colF:
        wall_u_value = st.number_input(" Wall U-Value(W/m².K)", min_value=0.000, value=0.000, max_value=3.000, format="%.2f")
    with colG:
        roof_u_value = st.number_input(" Roof U-Value(W/m².K)", min_value=0.000, value=0.000, max_value=3.000, format="%.2f")
    colH, colhh = st.columns(2)
    with colH:
        window_u_value = st.number_input(" Window U-Value(W/m².K)", min_value=0.000, value=1.599, max_value=6.000, format="%.2f")
    with colhh:
        undergrndWall_u_value = st.number_input("Underground Wall U-Value(W/m².K)", min_value=0.000, value=1.599, max_value=3.000, format="%.2f")

    # Internal Loads
    st.markdown('<div class="section-header"> Internal Loads</div>', unsafe_allow_html=True)

    colI, colJ = st.columns(2)
    with colI:
        lighting_load = st.number_input("Power Lighting (W/m²)", min_value=0.000, value=0.000, max_value = 10.00, format="%.2f")
    with colJ:
        equipment_load = st.number_input("Equipment Total (W/m²)", min_value=0.000, value=0.00, max_value=20.00, format="%.2f")
    # with colK:
    total_lsc = 0.005
    total_load = 0.0232
    # with colL:
    #     total_load = st.number_input("Total-LOAD(kW)", min_value=0.000, value=15.099, format="%.3f")

    # Predict Button
    st.markdown("<br>", unsafe_allow_html=True)
    predict_button = st.button("🔍 Predict Energy Performance", type="primary")

# ---------------- RIGHT COLUMN (Outputs) ----------------
# Load the trained model, scaler, and preprocessor
with bz2.BZ2File('energy_prediction_model.pbz2', 'rb') as file:
    data = pickle.load(file)
    model = data['model']
    scaler = data['scaler']
    preprocessor = data['preprocessor']

# Preprocess input function
def preprocess_input(data, scaler, preprocessor):
    data[cols_to_scale] = scaler.transform(data[cols_to_scale])
    encoded_data = preprocessor.transform(data)
    onehot_columns = preprocessor.transformers_[0][1].get_feature_names_out(categorical_features)
    return pd.DataFrame(encoded_data, columns=list(onehot_columns) + list(data.drop(columns=categorical_features).columns))

# Prediction Section
with colB:
    st.markdown('<div class="section-header" style="font-size: 22px; font-weight: bold; color: red; margin-bottom: 20px;">🔎 Predicted Outputs</div>', unsafe_allow_html=True)
    if predict_button:
        user_df = pd.DataFrame([{
            'Above-Grade/Below-Grade': above_grade_area / (below_grade_area if below_grade_area > 0 else 1),  # Avoid division by zero
            'Conditioned-Area/UnConditioned-Area': cond_area / (uncond_area if uncond_area > 0 else 1),
            'Roof-Area/Total-AG-Floor-Area': roof_area / (above_grade_area if above_grade_area > 0 else 1),
            'Total-Above-Grade-Ext-Wall-Area/Total-AG-FloorArea': wall_tot_ag_area / (above_grade_area if above_grade_area > 0 else 1),
            'Power-Lighting(W/SQFT)': lighting_load/10.7639,
            'Equipment-Tot(W/SQFT)': equipment_load/10.7639,
            'ROOF-U-Value(BTU/HR-SQFT-F)': roof_u_value*0.1761,  # Convert W/m²·K to BTU/hr·ft²·F
            'ALL WALLS-Wall-U-Value(BTU/HR-SQFT-F)': wall_u_value * 0.1761,
            'UNDERGRND-Wall-U-Value(BTU/HR-SQFT-F)': undergrndWall_u_value* 0.1761,
            'ROOF-Window-U-Value(BTU/HR-SQFT-F)': window_u_value*0.1761,
            'ALL WALLS-Window-U-Value(BTU/HR-SQFT-F)': window_u_value*0.1761,
            'WWR': window_wall_ratio,
            'Total-LSC(KW/SQFT)': total_lsc/(above_grade_area*10.7639+below_grade_area*10.7639),
            'Total-LOAD(KW/SQFT)': total_load/(above_grade_area*10.7639+below_grade_area*10.7639),
            'Total-LOAD/Conditioned-Area(KW/SQFT)': total_lsc / (cond_area*10.7639 if cond_area*10.7639 > 0 else 1),
            'Climate': climate  # This is your categorical feature
        }])
        cols_to_scale = [
            'Above-Grade/Below-Grade', 'Conditioned-Area/UnConditioned-Area', 'Roof-Area/Total-AG-Floor-Area',
            'Total-Above-Grade-Ext-Wall-Area/Total-AG-FloorArea', 'Power-Lighting(W/SQFT)', 'Equipment-Tot(W/SQFT)',
            'ROOF-U-Value(BTU/HR-SQFT-F)', 'ALL WALLS-Wall-U-Value(BTU/HR-SQFT-F)', 'UNDERGRND-Wall-U-Value(BTU/HR-SQFT-F)',
            'ROOF-Window-U-Value(BTU/HR-SQFT-F)', 'ALL WALLS-Window-U-Value(BTU/HR-SQFT-F)', 'WWR',
            'Total-LSC(KW/SQFT)', 'Total-LOAD(KW/SQFT)', 'Total-LOAD/Conditioned-Area(KW/SQFT)'
        ]
        categorical_features = ['Climate']

        processed_input = preprocess_input(user_df, scaler, preprocessor)
        prediction = model.predict(processed_input)
        st.success("✅ Prediction Complete")
        # st.success(f"Predicted Energy Outcome (KWH/SQFT): {prediction[0]:.4f}")
        eui = prediction[0]*10.7639
        if eui > 150:
            energy_outcome = "High"
        elif(eui <= 150 and eui > 120):
            energy_outcome = "Medium"
        else:
            energy_outcome = "Low"
        peak_load = 0.2561*10.7639

        # Use container to style and align metrics in a single row
        with st.container():
            st.markdown(
                f"""
                <style>
                .metric-container {{
                    display: flex;
                    justify-content: space-between;
                    gap: 20px;
                    margin: 10px 0;
                }}
                .metric-box {{
                    flex: 1;
                    padding: 15px;
                    background-color: #f1f3f6;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .metric-label {{
                    font-weight: bold;
                    font-size: 14px;
                    margin-bottom: 5px;
                    color: #333;
                }}
                .metric-value {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #007BFF;
                }}
                </style>
                
                <div class="metric-container">
                    <div class="metric-box">
                        <div class="metric-label">🔋 EUI (kWh/m².Yr)</div>
                        <div class="metric-value">{eui:.4f}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">🌍 Energy Outcome</div>
                        <div class="metric-value">{energy_outcome}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">⚡ Peak Load (kW/m²)</div>
                        <div class="metric-value">{peak_load:.4f}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Download button with PDF report
        pdf_bytes = generate_pdf_report(eui, energy_outcome, peak_load)
        st.download_button(label="📥 Download Report (PDF)", data=pdf_bytes, file_name="energy_performance_report.pdf", mime="application/pdf")
    
    else:
        st.info("👈 Fill the inputs and click **Predict Energy Performance** to generate predictions.")

# Footer
st.markdown("---")
st.markdown('<div class="footer">👨‍💻 Developed as part of Machine Learning Energy Modeling Application | © 2025</div>', unsafe_allow_html=True)