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
#for recommendations
def get_recommendations(user_preferences, data_encoded,n):
    user_vector = np.array(list(user_preferences.values())).reshape(1, -1)

    cosine_similarities = []
    for i in range(len(data_encoded)):
        exc_vector = data_encoded.iloc[i, 3:].values.reshape(1, -1)
        similarity = cosine_similarity(exc_vector, user_vector)
        cosine_similarities.append(similarity[0][0])
    data_encoded_copy = data_encoded.copy(deep=True)
    data_encoded_copy['Cosine_Similarity'] = cosine_similarities

    data_encoded_sorted = data_encoded_copy.sort_values(by='Cosine_Similarity', ascending=False)
    recommended_exercises_with_highest_similarity = data_encoded_sorted[
        data_encoded_sorted['Cosine_Similarity'] == data_encoded_sorted['Cosine_Similarity'].max()
    ]

    shuffled_recommended_exercises = recommended_exercises_with_highest_similarity.sample(frac=1).reset_index(drop=True)
    top_10_recommended_exercises = shuffled_recommended_exercises.head(n)
    data = top_10_recommended_exercises.to_dict(orient='records')

    transformed_records = []
    for record in data:
        new_record = {key: record[key] for key in ['Title', 'Desc']}
        new_record['encoded_values'] = {key: value for key, value in record.items() if key not in ['Title', 'Desc', 'Cosine_Similarity']}
        
        if record.get('Type_Strength') == 1:
            if record.get('Level_Beginner') == 1:
                new_record['reps'] = '7-10'
                new_record['sets'] = '2-3'
            elif record.get('Level_Expert') == 1:
                new_record['reps'] = '8-12'
                new_record['sets'] = '3-4'
            elif record.get('Level_Intermediate') == 1:
                new_record['reps'] = '10-14'
                new_record['sets'] = '4-5'
        
        transformed_records.append(new_record)
    
    return transformed_records

transformed_records=get_recommendations(user_preferences,data_encoded,10)

#Recommendations based on selected excersises.
def get_recommendations_for_selected_indices(selected_indices, transformed_data, user_preferences, data_encoded, n):
    def get_encoded_values_by_indices(selected_indices, transformed_data):
        encoded_vectors = []
        for index in selected_indices:
            if index < len(transformed_data):
                encoded_values = transformed_data[index]['encoded_values']
                # Remove the 'Unnamed: 0' key if present
                encoded_values.pop('Unnamed: 0', None)
                encoded_vectors.append(encoded_values)
        return encoded_vectors
    
    def get_unique_dicts(dicts):
        unique_dicts = []
        for d in dicts:
            if d not in unique_dicts:
                unique_dicts.append(d)
        return unique_dicts
    
    encoded_vectors = get_encoded_values_by_indices(selected_indices, transformed_data)
    unique_dicts = get_unique_dicts(encoded_vectors)
    
    results = []
    for unique_dict in unique_dicts:
        result = get_recommendations(user_preferences, data_encoded, n)
        results.append(result)
    
    return results


selected_indices = [0, 1, 2]  # Example indices of the exercises selected by the user
results = get_recommendations_for_selected_indices(selected_indices, transformed_records, user_preferences, data_encoded, 5)
print(results)
