import streamlit as st
from user_auth import userAuth as user_auth
import hydralit_components as hc

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


def side_bar_user_info():    
    st.sidebar.write("User Information")
    age = st.sidebar.selectbox("Age", [i for i in range(1, 100)])
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    ht = st.sidebar.selectbox("Height (cm)", [i for i in range(100, 250)])
    wt = st.sidebar.selectbox("Weight (kg)", [i for i in range(30, 200)])
    level =  st.sidebar.selectbox("Activity Level", ["Beginer", "Intermediate", "Advanced"])
    type = st.sidebar.selectbox("Goal", ["Weight Loss", "Weight Gain", "Maintain Weight"])
    submit = st.sidebar.button("Submit")
    return age, gender, ht, wt, level, type, submit

def dashboard_content():
    age, gender, ht, wt, level, type, submit = side_bar_user_info()
    over_theme = {'txc_inactive': 'white','menu_background':'purple','txc_active':'yellow','option_active':'blue'}
    font_fmt = {'font-class':'h2','font-size':'150%'}
    op = hc.option_bar(option_definition=[{"label": "workout"}, {"label": "nutrition"}, {"label": "profile"}], override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)
    
        

if __name__ == "__main__":
    st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
    access_token = True
    if access_token:
        
        dashboard_content()
       # st.rerun()