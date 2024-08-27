import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from pathlib import Path

def load_data():
    """Loads data from the 'assets' directory and returns the relevant datasets."""
    assets_path = Path(__file__).parent / 'assets'
    crops_data = pd.read_csv(assets_path / 'crops_data.csv')
    soil_data = pd.read_csv(assets_path / 'soil_data.csv')
    pest_pathogen_data = pd.read_csv(assets_path / 'pest_pathogen_data.csv')
    fertilizers_data = pd.read_csv(assets_path / 'fertilizers_data.csv')
    return crops_data, soil_data, pest_pathogen_data, fertilizers_data

def train_productivity_model(data):
    """Train a model to predict crop productivity based on soil conditions."""
    X = data[['soil_nitrogen', 'soil_phosphorus', 'soil_potassium', 
              'soil_moisture', 'soil_ph', 'organic_matter']].values
    y = data['production'].values
    model = LinearRegression().fit(X, y)
    return model

def train_fertilizer_model(data):
    """Train a model to predict fertilizer quantity based on soil and crop conditions."""
    # Choose features for fertilizer prediction (adjust features as needed)
    X = data[['soil_nitrogen', 'soil_phosphorus', 'soil_potassium', 
              'soil_moisture', 'soil_ph', 'organic_matter']].values
    y = data['quantity'].values
    model = LinearRegression().fit(X, y)
    return model

def app():
    """Main function to run the Streamlit app."""
    crops_data, soil_data, pest_pathogen_data, fertilizers_data = load_data()

    id_column = 'id'
    if id_column not in crops_data.columns or id_column not in soil_data.columns:
        st.error(f"'{id_column}' column not found in the datasets. Please check the column names.")
        return

    # Merge crops_data with soil_data and fertilizers_data for alignment
    data = pd.merge(soil_data, crops_data[[id_column, 'production']], on=id_column)
    data = pd.merge(data, fertilizers_data[[id_column, 'quantity']], on=id_column)

    # Train models for both productivity and fertilizer prediction
    productivity_model = train_productivity_model(data)
    fertilizer_model = train_fertilizer_model(data)

    # Create tabs for different sections
    tabs = st.tabs(["Crops Overview", "Soil Conditions", "Pest and Pathogen", "Fertilizers"])

    with tabs[0]:
        st.header("Crops Overview")
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
            current_production = data['production'].values
            productivity_predictions = productivity_model.predict(data[['soil_nitrogen', 'soil_phosphorus', 
                                                                         'soil_potassium', 'soil_moisture', 
                                                                         'soil_ph', 'organic_matter']].values)

            comparison_df = pd.DataFrame({
                'Field ID': data[id_column],
                'Current Production': current_production,
                'Predicted Productivity': productivity_predictions
            })

            fig = px.line(comparison_df, x='Field ID', y=['Current Production', 'Predicted Productivity'],
                          title="Current vs Predicted Productivity per Field",
                          labels={'value': 'Production', 'variable': 'Type'},
                          markers=True)
            st.plotly_chart(fig)

    with tabs[3]:
        st.header("Fertilizers Overview")
        st.write("""
        This section provides insights into the application of fertilizers in various fields, 
        including predictions for future fertilizer needs based on soil and crop conditions.
        """)

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
            if 'date' in fertilizers_data.columns:
                fertilizers_data['date'] = pd.to_datetime(fertilizers_data['date'], errors='coerce')
                fertilizers_data['quantity'] = pd.to_numeric(fertilizers_data['quantity'], errors='coerce')
                fertilizers_data_clean = fertilizers_data.dropna(subset=['date', 'quantity'])

                fig = px.line(fertilizers_data_clean, x='date', y='quantity', color='type',
                              title="Fertilizer Quantity Over Time")
                st.plotly_chart(fig)
            else:
                st.error("Date column not found in fertilizers_data. Please ensure the data contains a 'date' column.")

        with row2:
            st.subheader("Fertilizer Prediction per Field")
            current_fertilizer_quantity = data['quantity'].values
            fertilizer_predictions = fertilizer_model.predict(data[['soil_nitrogen', 'soil_phosphorus', 
                                                                     'soil_potassium', 'soil_moisture', 
                                                                     'soil_ph', 'organic_matter']].values)

            fertilizer_comparison_df = pd.DataFrame({
                'Field ID': data[id_column],
                'Current Fertilizer Quantity': current_fertilizer_quantity,
                'Predicted Fertilizer Quantity': fertilizer_predictions
            })

            fig = px.line(fertilizer_comparison_df, x='Field ID', 
                          y=['Current Fertilizer Quantity', 'Predicted Fertilizer Quantity'],
                          title="Current vs Predicted Fertilizer Quantity per Field",
                          labels={'value': 'Fertilizer Quantity', 'variable': 'Type'},
                          markers=True)
            st.plotly_chart(fig)

if __name__ == "__main__":
    app()
