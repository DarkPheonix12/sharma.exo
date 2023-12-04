# import streamlit as st
# from streamlit_option_menu import option_menu
# import home, trending, test, your, about
# from test import *
# from firebase_admin import credentials


# st.set_page_config(
#     page_title="Pondering",
# )

# class MultiApp:

#     def __init__(self):
#         self.apps = []

#     def add_app(self, title, func):
#         self.apps.append({
#             "title": title,
#             "function": func
#         })

#     def run(self):  # Add self as the first parameter
#         with st.sidebar:
#             app = option_menu(
#                 menu_title='Pondering ',
#                 options=['Home','Account','Trending','Your Posts','about'],
#                 icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
#                 menu_icon='chat-text-fill',
#                 default_index=1,
#                 styles={
#                     "container": {"padding": "5!important","background-color":'black'},
#                     "icon": {"color": "white", "font-size": "23px"}, 
#                     "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
#                     "nav-link-selected": {"background-color": "#02ab21"},
#                 }
#             )
        
#         if app == "Home":
#             home.app()
#         if app == "Account":
#             test.app()    
#         if app == "Trending":
#             trending.app()        
#         if app == 'Your Posts':
#             your.app()
#         if app == 'about':
#             about.app()    

# # Create an instance of MultiApp
# multi_app = MultiApp()

# # Add your apps to the MultiApp
# multi_app.add_app("Home", home.app)
# multi_app.add_app("Account", test.app)
# multi_app.add_app("Trending", trending.app)
# multi_app.add_app("Your Posts", your.app)
# multi_app.add_app("About", about.app)

# # Run the MultiApp
# multi_app.run()

import streamlit as st
from streamlit_option_menu import option_menu
import home, trending, test, your, about
from firebase_admin import credentials
from firebase_admin import firestore


st.set_page_config(
    page_title="Au-Table",
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self, db):  # Pass the Firestore client as an argument
        with st.sidebar:
            app = option_menu(
                menu_title='Au-table',
                options=['Home', 'Account', 'Trending', 'Your Posts', 'about'],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if app == "Home":
            home.app()
        if app == "Account":
            test.app()
        if app == "Trending":
            trending.app(db)  # Pass the Firestore client to the trending app
        if app == 'Your Posts':
            your.app()
        if app == 'about':
            about.app()

# Create an instance of MultiApp
multi_app = MultiApp()

# Add your apps to the MultiApp
multi_app.add_app("Home", home.app)
multi_app.add_app("Account", test.app)
multi_app.add_app("Trending", trending.app)
multi_app.add_app("Your Posts", your.app)
multi_app.add_app("About", about.app)

# Run the MultiApp
if __name__ == "__main__":
    db_instance = firestore.client()  # Initialize your Firestore client
    multi_app.run(db_instance)
