import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_data():
    # Load the CSV files from the 'assets' directory
    livestock_data = pd.read_csv(os.path.join('assets', 'livestock_data.csv'))
    health_check_data = pd.read_csv(os.path.join('assets', 'health_check_data.csv'))
    return livestock_data, health_check_data

def app():
    # Load data
    livestock_data, health_check_data = load_data()

    # Create tabs
    tabs = st.tabs(["Livestock Overview", "Animal Health Check"])

    with tabs[0]:
        st.header("Livestock Overview")
        st.write("""
        This section provides an overview of the livestock data, including details about different animals, their age in months, 
        and their current status. The data helps in understanding the distribution and demographics of the livestock.
        """)
        
        # Create layout for graphs
        col1, col2 = st.columns(2)
        row1, row2 = st.columns(2)

        with col1:
            st.subheader("Livestock Distribution by Animal Type")
            fig = px.pie(livestock_data, names='animal', title="Livestock Distribution by Animal Type", hole=0.4)
            st.plotly_chart(fig)

        with col2:
            st.subheader("Age Distribution of Livestock")
            fig = px.histogram(livestock_data, x='age(months)', title="Age Distribution of Livestock", nbins=20)
            st.plotly_chart(fig)

        with row1:
            st.subheader("Gender Distribution")
            fig = px.bar(livestock_data, x='gender', title="Gender Distribution of Livestock")
            st.plotly_chart(fig)

        with row2:
            st.subheader("Pregnancy Status")
            fig = px.pie(livestock_data, names='pregnant', title="Pregnancy Status of Livestock", hole=0.4)
            st.plotly_chart(fig)

    with tabs[1]:
        st.header("Animal Health Check")
        st.write("""
        This section provides insights into the health checks conducted on the livestock, including details about vaccines administered,
        diseases monitored, and trends over time. Understanding these aspects is crucial for effective health management of the animals.
        """)
        
        # Create layout for graphs
        col1, col2 = st.columns(2)
        row1, row2 = st.columns(2)

        with col1:
            st.subheader("Vaccines Administered")
            # Count the number of vaccines administered
            vaccines_count = health_check_data['vaccines'].value_counts().reset_index()
            vaccines_count.columns = ['Vaccine', 'Count']
            fig = px.bar(vaccines_count, x='Vaccine', y='Count', title="Vaccines Administered")
            st.plotly_chart(fig)

        with col2:
            st.subheader("Diseases Diagnosed")
            # Count the occurrences of each disease
            diseases_series = health_check_data['diseases'].str.split(',', expand=True).stack()
            diseases_count = diseases_series.value_counts().reset_index()
            diseases_count.columns = ['Disease', 'Count']
            fig = px.bar(diseases_count, x='Disease', y='Count', title="Diseases Diagnosed")
            st.plotly_chart(fig)

        with row1:
            st.subheader("Health Check Trends Over Time")
            # Convert check_date to datetime and plot trends
            health_check_data['check_date'] = pd.to_datetime(health_check_data['check_date'])
            fig = px.line(health_check_data, x='check_date', y='id', title="Health Check Trends Over Time", markers=True)
            st.plotly_chart(fig)

        with row2:
            st.subheader("Vaccines vs Diseases")
            # Create a combined DataFrame for vaccines and diseases
            vaccines_diseases_df = health_check_data.copy()
            vaccines_diseases_df['vaccines'] = vaccines_diseases_df['vaccines'].str.split(',').apply(len)
            vaccines_diseases_df['diseases'] = vaccines_diseases_df['diseases'].str.split(',').apply(len)
            fig = px.scatter(vaccines_diseases_df, x='vaccines', y='diseases', color='check_date',
                             title="Vaccines vs Diseases", labels={'vaccines': 'Number of Vaccines', 'diseases': 'Number of Diseases'})
            st.plotly_chart(fig)

if __name__ == "__main__":
    app()
import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker to generate random dates
faker = Faker()

# Define sample data for farming practices and emissions types
farming_practices = ['Livestock', 'Fertilizer Application', 'Soil Management']
emissions_types = ['Methane', 'CO2', 'N2O']

# Define the header of the CSV file based on the table schema
header = ['Farm_ID', 'Farming_Practice', 'Emissions_Type', 'Emissions_Amount', 'Date']

# Number of rows you want to generate
num_rows = 100

# Function to generate random emissions amount
def generate_emissions_amount(practice):
    if practice == 'Livestock':
        return round(random.uniform(10, 50), 2)  # Methane emissions in metric tons
    elif practice == 'Fertilizer Application':
        return round(random.uniform(5, 30), 2)   # CO2 emissions in metric tons
    elif practice == 'Soil Management':
        return round(random.uniform(2, 15), 2)   # N2O emissions in metric tons
    return 0

# Generate data
data = []
for i in range(1, num_rows + 1):
    # Generate a unique farm ID
    farm_id = f"FARM-{i:04d}"
    
    # Randomly choose farming practice
    practice = random.choice(farming_practices)
    
    # Randomly choose emissions type based on farming practice
    if practice == 'Livestock':
        emissions_type = 'Methane'
    elif practice == 'Fertilizer Application':
        emissions_type = 'CO2'
    elif practice == 'Soil Management':
        emissions_type = 'N2O'
    
    # Generate random emissions amount
    emissions_amount = generate_emissions_amount(practice)
    
    # Generate a random date within the past 5 years
    date = faker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
    
    # Create row of data
    row = {
        'Farm_ID': farm_id,
        'Farming_Practice': practice,
        'Emissions_Type': emissions_type,
        'Emissions_Amount': emissions_amount,
        'Date': date
    }
    data.append(row)

# Write the data to a CSV file
csv_file = 'emissions_data.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

print(f"Data successfully written to {csv_file}")

