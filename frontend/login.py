import random

import streamlit as st
from user_auth import userAuth as user_auth
from streamlit_option_menu import option_menu
from fetch_data_w_api import fetch_api_data
import api_payloads as ap
import hydralit_components as hc
import pandas as pd


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


def set_exercise_preference(level, type, eq, body_part):
    excercise_search_payload = ap.excercise_search_payload
    excercise_search_payload["Level_Beginner"] = "1" if level == "Beginer" else "0"
    excercise_search_payload["Level_Intermediate"] = "1" if level == "Intermediate" else "0"
    excercise_search_payload["Level_Expert"] = "1" if level == "Advanced" else "0"
    excercise_search_payload["Type_Cardio"] = "1" if type == "Endurance" else "0"
    excercise_search_payload["Type_Strength"] = "1" if type == "Strength" else "0"
    excercise_search_payload["Type_Stretching"] = "1" if type == "Flexibility" else "0"
    excercise_search_payload['Equipment_Gym'] = "1" if eq == "Gym" else "0"
    excercise_search_payload['Equipment_Body_Only'] = "1" if eq == "Body Weight" else "0"
    excercise_search_payload["BodyPart_Abdominals"] = "1" if body_part == "Abdominals" else "0"
    excercise_search_payload["BodyPart_Biceps"] = "1" if body_part == "Biceps" else "0"
    excercise_search_payload["BodyPart_Chest"] = "1" if body_part == "Chest" else "0"
    excercise_search_payload["BodyPart_Forearms"] = "1" if body_part == "Forearms" else "0"
    excercise_search_payload["BodyPart_Neck"] = "1" if body_part == "Neck" else "0"
    excercise_search_payload["BodyPart_Shoulders"] = "1" if body_part == "Shoulders" else "0"
    excercise_search_payload["BodyPart_Triceps"] = "1" if body_part == "Triceps" else "0"
    excercise_search_payload["BodyPart_Legs"] = "1" if body_part == "Legs" else "0"
    excercise_search_payload["BodyPart_Back"] = "1" if body_part == "Back" else "0"
    excercise_search_payload["BodyPart_FullBody"] = "1" if body_part == "Full body" else "0"
    return excercise_search_payload


def set_diet_preference(calories, protien, max_time, alergies):
    diet_search_payload = ap.diet_search_payload
    diet_search_payload["Calories"] = str(calories)
    diet_search_payload["ProteinContent"] = str(protien)
    diet_search_payload["MaxTime"] = str(max_time)
    diet_search_payload["Allergies"] = alergies
    return diet_search_payload


def side_bar_exercise_search():
    st.sidebar.title("Search Exercises")
    level = st.sidebar.selectbox("Activity Level", ["Beginer", "Intermediate", "Advanced"])
    type = st.sidebar.selectbox("Goal", ["Endurance", "Strength", "Flexibility", ])
    eq = st.sidebar.selectbox("Equipment", ["Gym", "Body Weight", "Bands"])
    body_part = st.sidebar.selectbox("Body Part",
                                     ["Abdominals", "Biceps", "Chest", "Forearms", "Neck", "Shoulders", "Triceps",
                                      "Legs",
                                      "Back", "FullBody"])
    submit = st.sidebar.button("Submit")

    if submit:
        st.divider()
        st.sidebar.subheader("Your Exercise Search Results")
        excercise_search_payload = set_exercise_preference(level, type, eq, body_part)
        fetch_api_data_obj = fetch_api_data(access_token)
        data = fetch_api_data_obj.fetch_data("http://127.0.0.1:8080/exercise/search", request_type="POST",
                                             data=excercise_search_payload)
        for item_data in data:
            workout_search_item(item_data)

        for k, v in excercise_search_payload.items():
            excercise_search_payload[k] = '0'


def side_bar_diet_search():
    st.sidebar.title("Search Diets")
    age = st.sidebar.selectbox("Age", [i for i in range(1, 100)], index=25)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"], index=0)
    ht = st.sidebar.selectbox("Height (cm)", [i for i in range(100, 250)], index=66)
    wt = st.sidebar.selectbox("Weight (kg)", [i for i in range(30, 200)], index=47)
    alergies = st.sidebar.text_input("Alergies")
    max_time = st.sidebar.selectbox("Max Time", [i for i in range(1, 100)], index=39)
    submit = st.sidebar.button("Submit")
    theme_bad = {'bgcolor': '#FFF0F0', 'title_color': 'red', 'content_color': 'red', 'icon_color': 'red',
                 'icon': 'fa fa-times-circle'}
    theme_neutral = {'bgcolor': '#f9f9f9', 'title_color': 'orange', 'content_color': 'orange', 'icon_color': 'orange',
                     'icon': 'fa fa-question-circle', 'font_size': '10px'}
    theme_good = {'bgcolor': '#EFF8F7', 'title_color': 'green', 'content_color': 'green', 'icon_color': 'green',
                  'icon': 'fa fa-check-circle', 'font_size': '20px'}

    # Calculate BMI
    height_in_meters = ht / 100
    weight_in_kg = wt
    bmi = weight_in_kg / (height_in_meters ** 2)

    # Calculate Protein Intake
    if gender == "Male":
        protein_intake = weight_in_kg * 1.2
    else:
        protein_intake = weight_in_kg * 0.8

    # Calculate Calories Required
    if gender == "Male":
        calories_required = (10 * weight_in_kg) + (6.25 * ht) - (5 * age) + 5
    else:
        calories_required = (10 * weight_in_kg) + (6.25 * ht) - (5 * age) - 161

    cols = st.columns([0.5, 0.5, 0.5])

    with cols[0]:
        if bmi < 18.5:
            hc.info_card(title="BMI", content=f"{bmi:.2f} bmi is low than expected", bar_value=int(bmi),
                         theme_override=theme_bad)
        elif bmi >= 18.5 and bmi < 24.9:
            hc.info_card(title="BMI", content=f"{bmi:.2f} bmi is normal", bar_value=bmi, sentiment="good")
        elif bmi >= 25 and bmi <= 29.9:
            hc.info_card(title="BMI", content=f"{bmi:.2f} bmi is overweight", bar_value=bmi, theme_override=theme_bad)
        elif bmi >= 30:
            hc.info_card(title="BMI", content=f"{bmi:.2f} bmi is obese", bar_value=bmi, theme_override=theme_bad)
    with cols[1]:
        hc.info_card(title="Protein Intake", content=f"{protein_intake:.2f} grams", bar_value=100, sentiment="neutral",
                     theme_override=theme_neutral)
    with cols[2]:
        hc.info_card(title="Calories", content=f"{calories_required:.2f} kcal", bar_value=100, sentiment="nuetral",
                     theme_override=theme_neutral)
    if submit:
        st.divider()
        st.subheader("Your Diet Search Results")
        diet_search_payload = set_diet_preference(calories_required, protein_intake, max_time, alergies)
        fetch_api_data_obj = fetch_api_data(access_token)
        data = fetch_api_data_obj.fetch_data("http://127.0.0.1:8080/food/search", request_type="POST",
                                             data=diet_search_payload)
        if data:
            df = pd.DataFrame(data)
            st.write("According to your preferences, here are some diet recommendations divide them as per your meal "
                     "plan")
            # st.write(df))

            view_df = df[['Name', 'RecipeIngredientParts', 'RecipeInstructions', 'TotalTime', 'Description', 'Calories',
                          'ProteinContent']]
            view_df['TotalTime'] = view_df['TotalTime'].apply(
                lambda x: x.split("T")[1].replace("H", ":").replace("M", ""))
            view_df['RecipeInstructions'] = view_df['RecipeInstructions'].apply(
                lambda x: eval(x.replace("c(", "[").replace(")", "]")))
            view_df['RecipeIngredientParts'] = view_df['RecipeIngredientParts'].apply(
                lambda x: eval(x.replace("c(", "[").replace(")", "]")))
            # from pprint import pprint
            # pprint(view_df.to_dict(orient="records")[0])

            for recipe_item in view_df.to_dict(orient="records"):
                print_recipe_details(recipe_item)
            # st.write(view_df)
        else:
            st.write("No diet recommendations could be generated based on your preferences.")


def print_recipe_details(recipe):
    with st.container(border=True):
        st.subheader(recipe["Name"])
        st.write(
            f"🕒 Time: {recipe['TotalTime']} mins \t 💪 Protein: {recipe['ProteinContent']} \t 🔥Calories: {recipe['Calories']}")
        st.markdown(f"#### Ingredients:\n{' '.join(['**' + ing + '**' for ing in recipe['RecipeIngredientParts']])}")
        st.markdown("#### Description:")
        st.write(recipe["Description"])
        st.markdown(f"#### Instructions:")
        st.markdown("\n".join(["- " + item for item in recipe["RecipeInstructions"]]), unsafe_allow_html=True)


def add_workout_search_item(exercise_id):
    fetch_api_data_obj = fetch_api_data(access_token)
    response = fetch_api_data_obj.fetch_data(
        "http://127.0.0.1:8080/exercise/log",
        request_type="POST",
        data={"exercise_id": exercise_id}
    )


def add_diet_search_item(food_id):
    fetch_api_data_obj = fetch_api_data(access_token)
    response = fetch_api_data_obj.fetch_data(
        "http://127.0.0.1:8080/food/log", request_type="POST", data={"food_id": food_id})


def diet_search_item(item_data):
    st.sidebar.subheader(item_data["Name"])
    st.sidebar.write(item_data["Description"])
    st.sidebar.write()

    st.sidebar.button(f"Add", key=item_data['food_id'], on_click=add_workout_search_item, args=(item_data['food_id'],))


def workout_search_item(item_data):
    with st.sidebar.container(border=True):
        st.subheader(item_data["title"])
        encoded_values = item_data['encoded_values']
        # Display in each column
        col1, col2, col3 = st.columns([1, 1, 1])
        for key, value in encoded_values.items():
            if value == 1:  # Only display if the value is 1
                if 'Level' in key:
                    col1.write(icons.get(key, "") + " " + key.replace("Level_", ""))
                elif 'Type' in key:
                    col2.write(icons.get(key, "") + " " + key.replace("Type_", ""))
                elif 'BodyPart' in key:
                    col3.write(icons.get(key, "") + " " + key.replace("BodyPart_", ""))

        col1, col2 = st.columns([1, 1])
        col1.write("Reps: " + item_data["reps"])
        col2.write("Sets: " + item_data["sets"])

        st.write(item_data["desc"])

        st.button(f"Add", key=str(item_data['exercise_id']) + "-" + str(random.randint(1, 99999)),
                  on_click=add_workout_search_item, args=(item_data['exercise_id'],))


def workout_recommendation_item(item_data):
    with st.container(border=True):
        st.subheader(item_data["title"])
        encoded_values = item_data['encoded_values']
        # Display in each column
        col1, col2, col3, _ = st.columns([1, 1, 1, 3])
        for key, value in encoded_values.items():
            if value == 1:  # Only display if the value is 1
                if 'Level' in key:
                    col1.write(icons.get(key, "") + " " + key.replace("Level_", ""))
                elif 'Type' in key:
                    col2.write(icons.get(key, "") + " " + key.replace("Type_", ""))
                elif 'BodyPart' in key:
                    col3.write(icons.get(key, "") + " " + key.replace("BodyPart_", ""))

        col1, col2, _ = st.columns([1, 1, 4])
        col1.write("Reps: " + item_data["reps"])
        col2.write("Sets: " + item_data["sets"])

        st.write(item_data["desc"])

        st.button(f"Add", key=str(item_data['exercise_id']) + "-" + str(random.randint(1, 99999)),
                  on_click=add_workout_search_item, args=(item_data['exercise_id'],))



icons = {
        "Level_Beginner": "🟢",
        "Level_Intermediate": "🟠",
        "Level_Expert": "🔴",
        "Type_Cardio": "🏃",
        "Type_Strength": "💪",
        "Type_Stretching": "🤸",
        "Equipment_Gym": "🏋️",
        "Equipment_Body_Only": "🧍"
    }


def dashboard_workout():
    side_bar_exercise_search()
    st.title("Workout Plan")

    # fetched logged workout exercises
    fetch_api_data_obj = fetch_api_data(access_token)
    data = fetch_api_data_obj.fetch_data("http://127.0.0.1:8080/exercise/history", request_type="GET")


    # st.sidebar.write(df)
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    col1.subheader("Exercise")
    col2.subheader("Difficulty Level")
    col3.subheader("Type")
    col4.subheader("Body Part")

    for item in data:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            col1.write(item['details']['title'])
            encoded_values = item['details']['encoded_values']
            # Display in each column
            for key, value in encoded_values.items():
                if value == 1:  # Only display if the value is 1
                    if 'Level' in key:
                        col2.write(icons.get(key, "") + " " + key.replace("Level_", ""))
                    elif 'Type' in key:
                        col3.write(icons.get(key, "") + " " + key.replace("Type_", ""))
                    elif 'BodyPart' in key:
                        col4.write(icons.get(key, "") + " " + key.replace("BodyPart_", ""))

    # fetch workout recommendations
    st.divider()
    st.title("Workout Recommendations")
    fetch_api_data_obj = fetch_api_data(access_token)
    data = fetch_api_data_obj.fetch_data("http://127.0.0.1:8080/exercise/recommendations/history", request_type="GET")
    if data:
        for item_data in data:
            workout_recommendation_item(item_data)

    else:
        st.write("No recommendations available based on your workout.")


def dashboard_diet():
    st.title("Diet Plan")
    side_bar_diet_search()


def dashboard_content():
    ms = option_menu(None, ["Workout", "Nutrition"],
                     icons=['bi-person-arms-up', 'bi-cup-hot-fill'],
                     menu_icon="cast", default_index=0, orientation="horizontal",
                     styles={
                         "container": {"padding": "1px", "background-color": "#fafafa", "color": "black"},
                         "icon": {"color": "orange", "font-size": "25px"},
                         "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                      "--hover-color": "#FFEBEE", "color": "black"},
                         "nav-link-selected": {"background-color": "#C62828", "color": "white"},
                     }
                     )
    if ms == "Workout":
        dashboard_workout()
    else:
        dashboard_diet()


if __name__ == "__main__":
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzczMTA3MzkzfQ.GWiE4vlXmUkP3OGeybufUTvliOsxBC82F9zIQ7sqHP4"
    if access_token:
        dashboard_content()
