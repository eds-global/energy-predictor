import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Building Energy Predictor",
    page_icon="🏙️", layout="wide", initial_sidebar_state="collapsed")
    
if st.button("Run Data Analysis"):
    @st.cache_data
    def load_data():
        df = pd.read_excel("database/NewNormalized_DB.xlsx")
        return df

    df = load_data()

    # Filter Business Typology
    business_df = df[df['ProjectTypology'] == 'Business'].drop(columns=['Climate', 'ProjectTypology'])
    business_df1 = df[df['ProjectTypology'] == 'Business'].drop(columns=['ProjectTypology'])

    # Statistical Summary Table
    def get_summary_statistics(df):
        summary = pd.DataFrame({
            'Min': df.min(),
            'Max': df.max(),
            'Mean': df.mean(),
            'Median': df.median()
        }).reset_index()
        summary.columns = ['Parameter', 'Min', 'Max', 'Mean', 'Median']
        return summary

    summary_stats = get_summary_statistics(business_df)

    st.markdown("##### Full Statistical Summary - Business Typology")
    st.dataframe(summary_stats, hide_index=True, use_container_width=True)

    # Outlier Detection
    def detect_outliers(df):
        outlier_summary = []
        for col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = ((df[col] < lower) | (df[col] > upper)).sum()
            outlier_summary.append([col, outliers])
        return pd.DataFrame(outlier_summary, columns=['Column', 'Outliers'])

    outlier_df = detect_outliers(business_df)

    with st.expander("🚨 Outlier Detection Report"):
        st.dataframe(outlier_df, hide_index=True)

    # Climate Filter
    climates = df['Climate'].unique()
    selected_climates = st.multiselect("🌎 Filter by Climate", climates, default=climates)

    filtered_df = df[(df['Climate'].isin(selected_climates)) & (df['ProjectTypology'] == 'Business')]

    st.markdown(f"##### 🔍 Filtered Data - {len(filtered_df)} Projects Selected")
    st.dataframe(filtered_df)

    # Ensure `Climate` column exists (business_df1 still has Climate)
    climate_col = [col for col in business_df1.columns if col.lower() == 'climate']
    if climate_col:
        climate_col = climate_col[0]
    else:
        st.error("No 'Climate' column found in dataset!")
        st.stop()

    # Numeric Columns (excluding Climate itself)
    numeric_columns = business_df1.select_dtypes(include=['number']).columns.tolist()

    # Energy Outcome column check
    energy_column = 'Energy_Outcome(KWH/SQFT)'
    if energy_column not in business_df1.columns:
        st.error(f"'{energy_column}' column is missing from the dataset!")
        st.stop()

    # Visualizations
    st.markdown("##### 📊 Data Visualizations - Business Typology")

    for col in numeric_columns:
        if col == energy_column:
            continue  # Skip plotting Energy Outcome against itself

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Histogram with Climate Hue
        sns.histplot(data=business_df1, x=col, hue=climate_col, kde=True, ax=axes[0], palette="Set2")
        # axes[0].set_title(f'Histogram of {col} with Climate')

        # Boxplot by Climate
        sns.boxplot(data=business_df1, x=climate_col, y=col, ax=axes[1], palette="Set2")
        # axes[1].set_title(f'Boxplot of {col} by Climate')

        # Scatter plot vs Energy Outcome
        sns.scatterplot(data=business_df1, x=col, y=energy_column, hue=climate_col, ax=axes[2], palette="Set2")
        # axes[2].set_title(f'Scatter plot of {col} vs {energy_column} (Colored by Climate)')

        st.pyplot(fig)