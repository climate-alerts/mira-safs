import streamlit as st
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Mira - Sustainability",
    layout="wide"
)

# Import app modules
import home, about, crops, livestock, maps, co2emission, weather

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Display the sidebar for navigation
        with st.sidebar:
            selected_app_title = option_menu(
                menu_title='Mira',
                options=[app["title"] for app in self.apps],
                icons=['house-fill', 'crops', 'sheep', 'satellite', 'cloud_upload', 'cloud_', 'personfill', 'infocircle'],
                menu_icon='local-florist',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": '#2f3030'},
                    "icon": {"color": "white", "font-size": "21px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#9d9ea1"},
                    "nav-link-selected": {"background-color": "#2f3030"}
                }
            )

        # Route to the selected page in the main content area
        for app_dict in self.apps:
            if app_dict["title"] == selected_app_title:
                app_dict["function"]()
                break

# Instantiate and run the MultiApp instance
app = MultiApp()

# Add apps to the MultiApp instance
app.add_app("Home", home.app)
app.add_app("About", about.app)
app.add_app("Crops", crops.app)
app.add_app("Livestock", livestock.app)
app.add_app("Maps", maps.app)
app.add_app("Emission", co2emission.app)
app.add_app("Weather", weather.app)

# Run the app
app.run()
