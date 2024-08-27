import streamlit as st
from pathlib import Path

def load_image_path():
    """Return the absolute path to the image."""
    # Use Path to safely manage file paths and handle different environments
    assets_path = Path(__file__).parent / 'assets' / 'field.jpg'
    
    # Check if the image exists
    if assets_path.is_file():
        return str(assets_path)
    else:
        return None

def app():
    # Set the title of the app
    st.title("Welcome to Mira Platform")

    # Load the image path
    image_path = load_image_path()

    # Display the main image or show an error if the image is not found
    if image_path:
        st.image(image_path, use_column_width=True)
    else:
        st.error("Image not found. Please check the 'assets/field.jpg' path and try again.")

    # Create tabs for different topics
    tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Key Features", "User Testimonials", "Get Started"])

    with tab1:
        st.header("Introduction")
        st.write("""
            The Sustainable Agricultural and Farm Security (SAFS) platform is a cutting-edge tool designed to revolutionize farm management. Mira integrates various aspects of farm management to promote streamlined and efficient agricultural practices.

            Explore our features:
            - **Field Monitoring**: Keep track of soil health, air quality, and crop conditions.
            - **Crop and Livestock Management**: Manage your crops and livestock with data-driven insights.
            - **Climate Data Analysis**: Analyze climate data to make informed decisions.
            - **Risk Assessment**: Evaluate risks such as drought and flooding to better prepare and respond.

            Discover how Mira can enhance your farming operations and contribute to sustainable agricultural practices.
        """)

    with tab2:
        st.header("Key Features")
        st.write("""
            - **Interactive Dashboards**: Visualize data through interactive graphs and charts.
            - **Data Insights**: Get actionable insights from real-time data analysis.
            - **Predictive Analytics**: Forecast future conditions and plan accordingly.
            - **User-Friendly Interface**: Easy-to-navigate design tailored for farm management.
        """)

    with tab3:
        st.header("User Testimonials")
        st.write("""
            *"Mira has transformed the way we manage our farm. The real-time data and insights are invaluable."* - Jane Doe, Farmer

            *"The predictive analytics feature has helped us prepare for adverse weather conditions, improving our yield significantly."* - John Smith, Agronomist
        """)

    with tab4:
        st.header("Get Started")
        st.write("""
            Ready to take your farm management to the next level? Get started with Mira today!

            [Contact Us](mailto:support@mira-farm.com) for more information or to schedule a demo.
        """)

        # Optional: Add a call to action button
        if st.button('Learn More'):
            st.write("""
                Visit our [website](https://www.mira-farm.com) to explore more about our platform and how it can benefit your farm.
            """)

# To run the app as the main entry point, use:
if __name__ == "__main__":
    app()

