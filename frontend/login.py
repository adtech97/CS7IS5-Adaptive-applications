import streamlit as st
from user_auth import userAuth as user_auth
import hydralit_components as hc
from fetch_data_w_api import fetch_api_data
import api_payloads as ap
import pandas as pd

def create_dataframe(response_data):
    df = pd.DataFrame(response_data)
    return df
def login():
    st.write("Login")
    user_name = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        auth = user_auth(user_name, password)
        access_token = auth.login()
        if access_token:
            st.write("Logged in")
            return access_token
    else:
        st.write("Invalid Credentials")

def set_exercise_preference(level, type, eq):
    excercise_search_payload = ap.excercise_search_payload
    excercise_search_payload["Level_Beginner"] = "1" if level == "Beginer" else "0"
    excercise_search_payload["Level_Intermediate"] = "1" if level == "Intermediate" else "0"
    excercise_search_payload["Level_Expert"] = "1" if level == "Advanced" else "0"
    excercise_search_payload["Type_Cardio"] = "1" if type == "Endurance" else "0"
    excercise_search_payload["Type_Strength"] = "1" if type == "Strength" else "0"
    excercise_search_payload["Type_Stretching"] = "1" if type == "Flixibility" else "0"
    excercise_search_payload['Equipment_Gym'] = "1" if eq == "Gym" else "0"
    excercise_search_payload['Equipment_Body_Only'] = "1" if eq == "Body Weight" else "0"
    excercise_search_payload["BodyPart_FullBody"] = "1" if type == "Full body" else "0"
    return excercise_search_payload


def side_bar_user_info():    
    st.sidebar.write("User Information")

    age = st.sidebar.selectbox("Age", [i for i in range(1, 100)])
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    ht = st.sidebar.selectbox("Height (cm)", [i for i in range(100, 250)])
    wt = st.sidebar.selectbox("Weight (kg)", [i for i in range(30, 200)])
    level =  st.sidebar.selectbox("Activity Level", ["Beginer", "Intermediate", "Advanced"])
    type = st.sidebar.selectbox("Goal", ["Endurance", "Strength", "Flixibility", "Full body"])
    eq = st.sidebar.selectbox("Equipment", ["Gym", "Body Weight", "Bands"])
    submit = st.sidebar.button("Submit")
    return age, gender, ht, wt, level, type, submit,eq

def dashboard_content_workout():
    age, gender, ht, wt, level, type, submit,eq = side_bar_user_info()
    over_theme = {'txc_inactive': 'black','menu_background':'white','txc_active':'Black','option_active':'Grey'}
    font_fmt = {'font-class':'h3','font-size':'95%'}
    ms = hc.nav_bar(menu_definition=[ {"label": "Workout"}, {"label": "Nutrition"}, {"label": "Profile"}], override_theme=over_theme, key="Primary_nav_bar")
    st.write(ms)
    if ms == "Workout" and submit:
        st.write("Your Workout Plan")
        excercise_search_payload = set_exercise_preference(level, type, eq)
        fetch_api_data_obj = fetch_api_data(access_token)
        data = fetch_api_data_obj.fetch_data("http://127.0.0.1:8080/exercise/search", request_type="POST", data=excercise_search_payload)
        df = create_dataframe(data)
        st.write(df)
        op2 = hc.option_bar(option_definition=[{"label": "Like"}, {"label": "Dislike"}], override_theme=over_theme,font_styling={'font-class':'h4','font-size':'90'},horizontal_orientation=True, key=
                           "option_bar_preference")
        #Reset the payload fields once workout is fetched
        for k, v in excercise_search_payload.items():
            excercise_search_payload[k] = '0'
     
        

if __name__ == "__main__":
    st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
    access_token = True
    if access_token:
        dashboard_content_workout()