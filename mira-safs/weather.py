import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load the climate data
def load_data():
    """Load the CSV file from the 'assets' directory."""
    assets_path = Path(__file__).parent / 'assets'
    csv_path = assets_path / 'climate_data.csv'
    return pd.read_csv(csv_path)

def app():
    # Load data
    data = load_data()

    # Create the Streamlit layout
    st.title("Climate Data Analysis")

    # Define the columns and rows layout
    col1, col2 = st.columns(2)
    row1, row2 = st.columns(2)

    with col1:
        st.header("Air Temperature vs. Soil Temperature")
        st.write("""
        This graph shows the relationship between air temperature and soil temperature.
        """)
        fig1 = px.scatter(data, x='air_temperature', y='soil_temperature', 
                          title="Air Temperature vs. Soil Temperature",
                          labels={'air_temperature': 'Air Temperature (°C)', 'soil_temperature': 'Soil Temperature (°C)'})
        st.plotly_chart(fig1)

    with col2:
        st.header("Soil Moisture vs. Air Moisture")
        st.write("""
        This graph shows the relationship between soil moisture and air moisture.
        """)
        fig2 = px.scatter(data, x='soil_moisture', y='air_moisture',
                          title="Soil Moisture vs. Air Moisture",
                          labels={'soil_moisture': 'Soil Moisture (%)', 'air_moisture': 'Air Moisture (%)'})
        st.plotly_chart(fig2)

    with row1:
        st.header("Rainfall Distribution")
        st.write("""
        This graph shows the distribution of rainfall amounts.
        """)
        fig3 = px.histogram(data, x='rain', nbins=20,
                            title="Distribution of Rainfall",
                            labels={'rain': 'Rainfall (mm)'})
        st.plotly_chart(fig3)

    with row2:
        st.header("Drought and Flooding Risk Distribution")
        st.write("""
        This graph shows the distribution of drought and flooding risks as percentages.
        """)
        # Create a DataFrame for risk distribution
        draught_counts = data[['draught_risk']].copy()
        draught_counts['Risk Type'] = 'Drought Risk'

        flooding_counts = data[['flooding_risk']].copy()
        flooding_counts['Risk Type'] = 'Flooding Risk'

        # Combine risk data for display
        combined_risks = pd.concat([draught_counts, flooding_counts], ignore_index=True)
        
        fig4 = px.histogram(combined_risks, x='draught_risk', color='Risk Type', nbins=20,
                            title="Distribution of Drought and Flooding Risks",
                            labels={'draught_risk': 'Risk Percentage'})
        st.plotly_chart(fig4)

if __name__ == "__main__":
    app()
