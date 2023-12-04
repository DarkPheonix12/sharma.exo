import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import pyrebase

# Initialize Firebase Admin for other Firebase services
cred = credentials.Certificate("timetable-7078c-84ae453a37d8.json")
firebase_admin.initialize_app(cred, name='Verfication')


config = {
    "apiKey": "AIzaSyAIb1t4wDgyABqKMPudkJqZ-IgsRaWKWOk",
    "authDomain": "timetable-7078c.firebaseapp.com",
    "projectId": "timetable-7078c",
    "databaseURL" : "https://timetable-7078c-default-rtdb.firebaseio.com/",
    "storageBucket": "timetable-7078c.appspot.com",
    "messagingSenderId": "484222065874",
    "appId": "1:484222065874:web:f360729ea1ed30d808210b",
    "measurementId": "G-011FS5SXL1"
}

firebase = pyrebase.initialize_app(config)

# Pyrebase auth object
auth = firebase.auth()

def app():
    st.title('Welcome to :violet[Time-Tables] :sunglasses:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    Usernm = ''  # Initialize Usernm

    def f(email, password):
        try:
            # Retrieve user by email using Pyrebase auth object
            user = auth.sign_in_with_email_and_password(email, password)
            
            # Additional checks can be performed if needed

            print(user['localId'])
            st.session_state.username = user['localId']
            st.session_state.useremail = email

            global Usernm
            Usernm = user['localId']

            st.session_state.signedout = True
            st.session_state.signout = True    
  
        except Exception as e:
            st.warning(f'Login Failed: {e}')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                user = auth.create_user_with_email_and_password(email, password, uid=username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            if st.button('Login') and email and password:
                f(email, password)

    if st.session_state.signout:
        st.text('UserName: ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

    def ap():
        st.write('Posts')
