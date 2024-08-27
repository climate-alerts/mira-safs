import streamlit as st

def local_css():
    st.markdown(
        """
        <style>
        /* Style for the tab container */
        .css-1v0mbdj {
            border-radius: 30px; /* Rounded corners for the entire tab container */
            overflow: hidden;
            border: 1px solid #ddd; /* Border around the tabs */
            padding: 10px; /* Padding around the tab container */
        }

        /* Style for tab headers */
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 24px;font-size: 2.4rem;/* Font size for the tab headers */
            font-weight: bold;
            border-radius: 10px 10px 0 0; /* Rounded top corners */
            margin: 0; /* Remove default margins */
            padding: 20px; /* Add padding */
            color: #FAAA19; /* Text color for inactive tabs */
        }

        /* Style for the active tab */
        .stTabs [data-baseweb="tab-list"] button[data-active="true"] {
            background-color: #15161A; /* Dark background for active tab */
            color: white; /* White text for active tab */
            border-radius: 10px 10px 0 0; /* Rounded top corners */
            font-weight: bold;
            border-bottom: 1px solid #15161A; /* Border below the active tab */
        }

        /* Optional: Hover effect for tabs */
        .stTabs [data-baseweb="tab-list"] button:hover {
            background-color: #000000; /* Light background on hover */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def app():
    # Inject custom CSS
    local_css()

    # Set up the title of the Streamlit app
    st.title("Mira - Sustainable Agriculture and Food Security")

    # Create tabs for each section
    tabs = st.tabs(["Overview", "About Mira", "Sustainable Farming", "Carbon Emission Reductions", "Features of SAFS"])

    # Overview Tab
    with tabs[0]:
        st.header("Welcome to the SAFS Platform")
        st.write(
            """
            The **Sustainable Agricultural and Farm Security (SAFS)** platform is your all-in-one solution for modern agricultural management. Designed to cater to the needs of contemporary farming, SAFS integrates various aspects of farm operations into a unified system, enhancing efficiency and productivity.
            """
        )

    # About Mira Tab
    with tabs[1]:
        st.header("About Mira")
        st.write(
            """
            **Mira** is a forward-thinking company dedicated to advancing sustainable agricultural practices and enhancing farm security through cutting-edge technology. Our mission is to empower farmers with innovative tools and insights that promote efficiency, productivity, and environmental stewardship. By leveraging data-driven solutions and advanced remote sensing technologies, Mira is committed to supporting the global transition towards more sustainable and responsible farming practices.
            """
        )

    # Sustainable Farming Tab
    with tabs[2]:
        st.header("Sustainable Farming")
        st.write(
            """
            Sustainable farming is an approach that seeks to balance agricultural productivity with environmental health, economic viability, and social equity. It involves practices that:
            
            - **Conserve Natural Resources:** Utilize resources like water, soil, and energy efficiently to reduce waste and preserve the environment.
            - **Enhance Soil Health:** Implement techniques that maintain or improve soil fertility and structure.
            - **Promote Biodiversity:** Support a diverse range of plant and animal life to create resilient agricultural ecosystems.
            - **Reduce Chemical Inputs:** Minimize the use of synthetic fertilizers and pesticides in favor of organic and natural alternatives.

            The SAFS platform supports sustainable farming by providing tools and data that help farmers make informed decisions and adopt practices that benefit both their operations and the environment.
            """
        )

    # Carbon Emission Reductions Tab
    with tabs[3]:
        st.header("Carbon Emission Reductions")
        st.write(
            """
            Reducing carbon emissions is crucial for mitigating climate change and fostering environmental sustainability. Agriculture contributes significantly to greenhouse gas emissions through activities like soil tillage, fertilizer application, and livestock management. SAFS helps farmers manage and reduce their carbon footprint by:

            - **Tracking Emissions:** Monitoring and quantifying emissions from various farm activities.
            - **Optimizing Practices:** Providing recommendations to minimize emissions and enhance carbon sequestration.
            - **Reporting and Accountability:** Offering tools to report emissions and track progress towards reduction goals.

            By integrating carbon emission accounting into the SAFS platform, we enable farmers to take proactive steps towards lowering their environmental impact and contributing to a more sustainable future.
            """
        )

    # Features of SAFS Tab
    with tabs[4]:
        st.header("Features of SAFS")
        st.write(
            """
            The SAFS platform offers a range of features designed to support comprehensive farm management:
            - **Field Management:** Add and manage farm fields with detailed information and adjustments.
            - **Crop Management:** Track and monitor crop types, health, and related metrics throughout their growth cycle.
            - **Soil Analysis:** Analyze soil samples and receive recommendations for improving soil quality and fertility.
            - **Livestock Monitoring:** Manage livestock health with regular checks and tracking to ensure well-being and productivity.
            - **Satellite Monitoring:** Use satellite data to analyze field conditions and crop health from a comprehensive perspective.
            - **Carbon Emission Accounting:** Track and manage carbon emissions from farm activities to work towards a reduced environmental impact.
            """
        )

    # Get Started with SAFS
    st.write(
        """
        **Experience the future of farm management with SAFS!** Explore the platform to transform your agricultural management experience. Whether you seek to improve efficiency, enhance sustainability, or gain deeper insights into farm operations, SAFS provides the tools you need to achieve your goals.
        """
    )

# Run the app function
if __name__ == "__main__":
    app()
