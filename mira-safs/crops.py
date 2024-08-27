import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from pathlib import Path

def load_data():
    """Loads data from the 'assets' directory and returns the relevant datasets."""
    # Define the path to the 'assets' directory
    assets_path = Path(__file__).parent / 'assets'

    # Load the CSV files from the 'assets' directory
    crops_data = pd.read_csv(assets_path / 'crops_data.csv')
    soil_data = pd.read_csv(assets_path / 'soil_data.csv')
    pest_pathogen_data = pd.read_csv(assets_path / 'pest_pathogen_data.csv')
    fertilizers_data = pd.read_csv(assets_path / 'fertilizers_data.csv')

    return crops_data, soil_data, pest_pathogen_data, fertilizers_data

def predict_productivity(soil_datarow, model):
    """Predict the productivity based on soil conditions."""
    features = soil_datarow[['soil_nitrogen', 'soil_phosphorus', 'soil_potassium', 
                             'soil_moisture', 'soil_ph', 'organic_matter']].values.reshape(1, -1)
    predicted_productivity = model.predict(features)
    return predicted_productivity[0]

def app():
    """Main function to run the Streamlit app."""
    # Load data
    crops_data, soil_data, pest_pathogen_data, fertilizers_data = load_data()

    # Check if 'id' column exists in the data
    id_column = 'id'
    if id_column not in crops_data.columns or id_column not in soil_data.columns:
        st.error(f"'{id_column}' column not found in the datasets. Please check the column names.")
        return

    # Merge crops_data with soil_data to align data based on 'id'
    data = pd.merge(soil_data, crops_data[[id_column, 'production']], on=id_column)

    # Train a model for predicting crop productivity based on soil conditions
    X = data[['soil_nitrogen', 'soil_phosphorus', 'soil_potassium', 
              'soil_moisture', 'soil_ph', 'organic_matter']].values
    y = data['production'].values
    model = LinearRegression().fit(X, y)

    # Create tabs for different sections
    tabs = st.tabs(["Crops Overview", "Soil Conditions", "Pest and Pathogen", "Fertilizers"])

    with tabs[0]:
        st.header("Crops Overview")
        st.write("""
        This section provides a comprehensive overview of the diverse crops cultivated in the fields, featuring visual representations of crop type distribution,
        historical production trends, and forecasts for future yields based on existing soil conditions.
        """)
        
        # 2x2 Layout for crop overview graphs
        col1, col2 = st.columns(2)
        row1, row2 = st.columns(2)

        with col1:
            st.subheader("Crop Type Distribution")
            fig = px.pie(crops_data, names='type', title="Crop Type Distribution", hole=0.4)
            st.plotly_chart(fig)

        with col2:
            st.subheader("Production Over Time")
            crops_data['production'] = pd.to_numeric(crops_data['production'], errors='coerce')
            fig = px.line(crops_data, x=id_column, y='production', title="Production Over Time")
            st.plotly_chart(fig)

        with row1:
            st.subheader("Production by Field")
            fig = px.bar(crops_data, x=id_column, y='production', title="Production by Field")
            st.plotly_chart(fig)

        with row2:
            st.subheader("Productivity Prediction per Field")
            # Get predicted and actual productivity values
            current_production = data['production'].values
            productivity_predictions = model.predict(X)

            # Create a DataFrame for comparison
            comparison_df = pd.DataFrame({
                'Field ID': data[id_column],
                'Current Production': current_production,
                'Predicted Productivity': productivity_predictions
            })

            # Plot the comparison graph
            fig = px.line(comparison_df, x='Field ID', y=['Current Production', 'Predicted Productivity'],
                          title="Current vs Predicted Productivity per Field",
                          labels={'value': 'Production', 'variable': 'Type'},
                          markers=True)
            st.plotly_chart(fig)

    with tabs[1]:
        st.header("Soil Conditions Overview")
        st.write("""
       This analysis summarizes soil conditions in various fields, emphasizing key indicators of soil health such as nutrient levels, pH, 
       moisture content, and organic matter. These elements are vital for assessing and enhancing crop productivity.
        """)
        
        # 2x2 Layout for soil condition graphs
        col1, col2 = st.columns(2)
        row1, row2 = st.columns(2)

        with col1:
            st.subheader("Soil Nutrient Levels by Field")
            nutrients = soil_data[[id_column, 'soil_nitrogen', 'soil_phosphorus', 'soil_potassium']]
            nutrients = nutrients.melt(id_vars=[id_column], var_name='Nutrient', value_name='Level')
            fig = px.bar(nutrients, x=id_column, y='Level', color='Nutrient', barmode='group',
                         title="Soil Nutrient Levels by Field")
            st.plotly_chart(fig)

        with col2:
            st.subheader("Soil pH Levels by Field")
            fig = px.bar(soil_data, x=id_column, y='soil_ph', title="Soil pH Levels by Field")
            st.plotly_chart(fig)

        with row1:
            st.subheader("Soil Moisture Content by Field")
            fig = px.bar(soil_data, x=id_column, y='soil_moisture', title="Soil Moisture Content by Field")
            st.plotly_chart(fig)

        with row2:
            st.subheader("Organic Matter by Field")
            fig = px.bar(soil_data, x=id_column, y='organic_matter', title="Organic Matter by Field")
            st.plotly_chart(fig)

    with tabs[2]:
        st.header("Pest and Pathogen Overview")
        st.write("""
        This analysis examines the effects of pests and pathogens on crop health in various fields, 
        emphasizing the level of damage incurred, the current containment measures, and the specific pests and pathogens identified, 
        thereby facilitating effective management and mitigation approaches.
        """)
        
        # 2x2 Layout for pest and pathogen graphs
        col1, col2 = st.columns(2)
        row1, row2 = st.columns(2)

        with col1:
            st.subheader("Area Damaged by Pest/Pathogen")
            fig = px.bar(pest_pathogen_data, x=id_column, y='area_damaged', color='pest_name', 
                         title="Area Damaged by Pest/Pathogen")
            st.plotly_chart(fig)

        with col2:
            st.subheader("Containment Status")
            fig = px.pie(pest_pathogen_data, names='status', title="Pest/Pathogen Containment Status")
            st.plotly_chart(fig)

        with row1:
            st.subheader("Pest/Pathogen by Field")
            fig = px.bar(pest_pathogen_data, x=id_column, y='pest_name', color='pathogen_name', 
                         title="Pest/Pathogen by Field")
            st.plotly_chart(fig)

        with row2:
            st.subheader("NDVI by Field")
            fig = px.bar(pest_pathogen_data, x=id_column, y='ndvi', title="NDVI by Field")
            st.plotly_chart(fig)

    with tabs[3]:
        st.header("Fertilizers Overview")
        st.write("""
       This section presents an analysis of fertilizer application in various fields, providing insights into the types, 
       amounts, and timing of fertilizer usage. Grasping these patterns is essential for enhancing crop yields and preserving soil health.
        """)
        
        # 2x2 Layout for fertilizers graphs
        col1, col2 = st.columns(2)
        row1, row2 = st.columns(2)

        with col1:
            st.subheader("Fertilizer Application by Type")
            fig = px.pie(fertilizers_data, names='type', values='quantity', title="Fertilizer Application by Type")
            st.plotly_chart(fig)

        with col2:
            st.subheader("Fertilizer Quantity by Field")
            fig = px.bar(fertilizers_data, x=id_column, y='quantity', color='type', title="Fertilizer Quantity by Field")
            st.plotly_chart(fig)

        with row1:
            st.subheader("Fertilizer Quantity Over Time")
            # Ensure 'date' column exists and is in correct format
            if 'date' in fertilizers_data.columns:
                fertilizers_data['date'] = pd.to_datetime(fertilizers_data['date'], errors='coerce')
                fertilizers_data['quantity'] = pd.to_numeric(fertilizers_data['quantity'], errors='coerce')
                fertilizers_data_clean = fertilizers_data.dropna(subset=['date', 'quantity'])
                
                # Plot Fertilizer Quantity Over Time
                fig = px.line(fertilizers_data_clean, x='date', y='quantity', color='type',
                              title="Fertilizer Quantity Over Time",
                              labels={'date': 'Date', 'quantity': 'Fertilizer Quantity'})
                st.plotly_chart(fig)
            else:
                st.error("Date column not found in fertilizers_data. Please ensure the data contains a 'date' column.")

        with row2:
            st.subheader("Fertilizer Application Prediction")
            # Placeholder for fertilizer prediction model
            fig = px.bar(fertilizers_data, x=id_column, y='quantity', title="Predicted Fertilizer Needs")
            st.plotly_chart(fig)

if __name__ == "__main__":
    app()

