import streamlit as st

st.set_page_config(
    page_title="Building Energy Predictor",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def landing_page():
    st.markdown(
        """
        <style>
            body {
                background-color: #f9f9f9;
            }
            .hero-container {
                text-align: center;
                padding: 50px 20px;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .main-title {
                font-size: 58px;
                font-weight: bold;
                color: #d72638;
                margin: 0;
                font-family: 'Arial', sans-serif;
            }
            .sub-title {
                font-size: 22px;
                color: #555;
                margin-top: 10px;
                font-family: 'Arial', sans-serif;
            }
            .cta-button {
                background-color: #d72638;
                color: white;
                padding: 18px 45px;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 20px;
            }
            .cta-button:hover {
                background-color: #b61d2d;
                transform: translateY(-3px);
            }
            .section-title {
                font-size: 32px;
                font-weight: bold;
                color: #d72638;
                margin: 60px 0 20px;
                font-family: 'Arial', sans-serif;
                text-align: center;
            }
            .feature-card {
                background-color: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                text-align: center;
                margin: 15px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                height: 100%;
            }
            .feature-card:hover {
                transform: translateY(-6px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }
            .feature-card h3 {
                color: #d72638;
                font-size: 20px;
                margin: 0 0 10px;
            }
            .feature-card p {
                color: #555;
                font-size: 15px;
            }
            .testimonial {
                font-style: italic;
                color: #444;
                background-color: #fff;
                padding: 20px;
                border-left: 4px solid #d72638;
                margin: 10px 0;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            .footer {
                font-size: 14px;
                text-align: center;
                margin-top: 50px;
                color: #888;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Hero Section
    st.markdown(
    """
    <style>
        .hero-container {
            text-align: center;
            padding: 50px 20px;
        }
        .main-title {
            font-size: 36px; /* reduced from a typical 48px or 50px */
            font-weight: bold;
            margin: 0;
        }
        .sub-title {
            font-size: 18px; /* reduced from around 24px */
            margin: 10px 0 30px;
            color: #555;
        }
        .cta-button {
            font-size: 14px; /* slightly smaller button text */
            padding: 10px 20px; /* smaller padding */
            background-color: red;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .cta-button:hover {
            background-color: #0056b3;
        }
    </style>
    <div class="hero-container">
        <h1 class="main-title">Building Energy Prediction</h1>
        <p class="sub-title">Smart Energy Insights for Smarter Decisions</p>
        <p>This application helps you predict the <b>Energy Performance</b> of a building based on inputs such as location,
         building typology, envelope characteristics, and internal loads.</p>
        <form action="/main" target="_self">
            <button class="cta-button" type="submit">Get Started Now</button>
        </form>
    </div>
    """,
    unsafe_allow_html=True
    )


    # Features Section
    st.markdown('<p class="section-title">Why Choose Us?</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Advanced Prediction</h3>
                <p>Accurate AI-powered forecasting to help you plan better and save costs.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Custom Reports</h3>
                <p>Instantly generate custom energy reports tailored to your building.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Seamless Integration</h3>
                <p>Works with your existing building management systems.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Cost Optimization</h3>
                <p>Identify energy-saving opportunities and reduce unnecessary expenses.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>User-Friendly Dashboard</h3>
                <p>Simple, intuitive interface for all users – no technical skills required.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>Expert Support</h3>
                <p>Our energy experts are just a call away to assist you.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Testimonials Section
    st.markdown('<p class="section-title">What Our Clients Say</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="testimonial">
                "Building Energy Prediction helped us cut down our energy bills by 18% within 4 months. Highly recommended!"
                <br><br>— Operations Manager, EcoBuild Corp.
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="testimonial">
                "The reports are not just insightful but easy to present to our stakeholders. It’s a game-changer for facility management."
                <br><br>— Facility Head, GreenSmart Properties
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="testimonial">
            "The future of energy efficiency is here. The insights have guided us in making smarter investment decisions."
            <br><br>— CEO, Urban Energy Solutions
        </div>
        """,
        unsafe_allow_html=True
    )

    # Footer
    st.markdown('<p class="footer">© 2025 Building Energy Prediction. All rights reserved.</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    landing_page()
