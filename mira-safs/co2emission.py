import streamlit as st
import pandas as pd
import plotly.express as px

# Load the climate data
def load_data():
    # Load the CSV file
    return pd.read_csv('assets/emissions_data.csv')

def app():
    # Load data
    data = load_data()

    # Create the Streamlit layout
    st.title("Climate Data Analysis")

    # Define the columns and rows layout
    col1, col2 = st.columns(2)
    row1, row2 = st.columns(2)

    with col1:
        st.header("Emissions by Farming Practice")
        st.write("""
        This graph shows the total emissions by different farming practices.
        """)
        # Check if the column exists before proceeding
        if 'Farming_Practice' in data.columns and 'Emissions_Amount' in data.columns:
            # Group by Farming_Practice and sum Emissions_Amount
            emissions_by_practice = data.groupby('Farming_Practice')['Emissions_Amount'].sum().reset_index()
            fig1 = px.bar(emissions_by_practice, x='Farming_Practice', y='Emissions_Amount',
                          title="Total Emissions by Farming Practice",
                          labels={'Farming_Practice': 'Farming Practice', 'Emissions_Amount': 'Total Emissions (kg CO2e)'})
            st.plotly_chart(fig1)
        else:
            st.error("Columns 'Farming_Practice' or 'Emissions_Amount' not found in data.")

    with col2:
        st.header("Emissions by Type")
        st.write("""
        This graph shows the distribution of emissions by type (e.g., N2O, CH4).
        """)
        # Check if the column exists before proceeding
        if 'Emissions_Type' in data.columns and 'Emissions_Amount' in data.columns:
            # Group by Emissions_Type and sum Emissions_Amount
            emissions_by_type = data.groupby('Emissions_Type')['Emissions_Amount'].sum().reset_index()
            fig2 = px.pie(emissions_by_type, names='Emissions_Type', values='Emissions_Amount',
                          title="Distribution of Emissions by Type",
                          labels={'Emissions_Type': 'Emissions Type', 'Emissions_Amount': 'Total Emissions (kg CO2e)'})
            st.plotly_chart(fig2)
        else:
            st.error("Columns 'Emissions_Type' or 'Emissions_Amount' not found in data.")

    with row1:
        st.header("Emissions Over Time")
        st.write("""
        This graph shows how emissions change over time.
        """)
        # Convert Date column to datetime
        if 'Date' in data.columns and 'Emissions_Amount' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            # Group by Date and sum Emissions_Amount
            emissions_over_time = data.groupby('Date')['Emissions_Amount'].sum().reset_index()
            fig3 = px.line(emissions_over_time, x='Date', y='Emissions_Amount',
                           title="Emissions Over Time",
                           labels={'Date': 'Date', 'Emissions_Amount': 'Total Emissions (kg CO2e)'})
            st.plotly_chart(fig3)
        else:
            st.error("Columns 'Date' or 'Emissions_Amount' not found in data.")

    with row2:
        st.header("Emissions by Energy Source")
        st.write("""
        This graph shows the total emissions by different energy sources.
        """)
        # Check if the column exists before proceeding
        if 'Energy_Source' in data.columns and 'Emissions_Amount' in data.columns:
            # Group by Energy_Source and sum Emissions_Amount
            emissions_by_energy_source = data.groupby('Energy_Source')['Emissions_Amount'].sum().reset_index()
            fig4 = px.bar(emissions_by_energy_source, x='Energy_Source', y='Emissions_Amount',
                          title="Total Emissions by Energy Source",
                          labels={'Energy_Source': 'Energy Source', 'Emissions_Amount': 'Total Emissions (kg CO2e)'})
            st.plotly_chart(fig4)
        else:
            st.error("Columns 'Energy_Source' or 'Emissions_Amount' not found in data.")

if __name__ == "__main__":
    app()

