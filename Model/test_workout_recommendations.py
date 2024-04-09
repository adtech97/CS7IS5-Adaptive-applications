from Model.workout_recommendations import WorkoutRecommendations
from pprint import pprint

user_preferences = {
    'Type_Cardio': 0,
    'Type_Strength': 1,
    'Type_Stretching': 0,
    'BodyPart_Abdominals': 0,
    'BodyPart_Biceps': 1,
    'BodyPart_Chest': 1,
    'BodyPart_Forearms': 0,
    'BodyPart_Neck': 0,
    'BodyPart_Shoulders': 1,
    'BodyPart_Triceps': 0,
    'Level_Beginner': 0,
    'Level_Expert': 0,
    'Level_Intermediate': 1,
    'Equipment_Gym': 1,
    'Equipment_Body_Only': 0,
    'BodyPart_Legs': 0,
    'BodyPart_Back': 0,
    'BodyPart_FullBody': 0,
}


def main():
    wrecs = WorkoutRecommendations("../Data/megaGymDataset.csv")

    # transformed_records = wrecs.get_recommendations(user_preferences, 10)
    #
    # pprint(transformed_records)

    selected_indices = [0] #, 1, 2]  # Example indices of the exercises selected by the user
    results = wrecs.get_recommendations_for_selected_indices(selected_indices, 5)
    print("Similar recommendations: ", len(results[0]))
    pprint(results)


if __name__ == "__main__":
    main()
