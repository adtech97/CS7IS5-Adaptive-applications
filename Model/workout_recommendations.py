import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class WorkoutRecommendations:
    def __init__(self, dataset_path):
        print("Reading data from {}".format(dataset_path))
        data = pd.read_csv(dataset_path)

        print("Processing dataset")
        data.drop(columns=['Rating', 'RatingDesc'], inplace=True)

        categorical_columns = ['Type', 'BodyPart', 'Equipment', 'Level']
        data_encoded = pd.get_dummies(data, columns=categorical_columns)

        data_encoded['Equipment_Gym'] = data_encoded[
            ['Equipment_Cable', 'Equipment_Machine', 'Equipment_E-Z Curl Bar', 'Equipment_Barbell',
             'Equipment_Dumbbell']].max(axis=1)
        data_encoded['Equipment_Bands'] = data_encoded['Equipment_Bands']  # Already in the desired format
        data_encoded['Equipment_Body_Only'] = data_encoded[
            'Equipment_Body Only']  # Assuming 'Body Only' is correct as per your dataset
        data_encoded['BodyPart_Legs'] = data_encoded[
            ['BodyPart_Quadriceps', 'BodyPart_Hamstrings', 'BodyPart_Calves', 'BodyPart_Glutes']].max(axis=1)
        data_encoded['BodyPart_Back'] = data_encoded[
            ['BodyPart_Lats', 'BodyPart_Lower Back', 'BodyPart_Middle Back']].max(axis=1)
        data_encoded['BodyPart_Chest'] = data_encoded['BodyPart_Chest']
        data_encoded['BodyPart_Shoulders'] = data_encoded[['BodyPart_Shoulders', 'BodyPart_Traps']].max(axis=1)

        data_encoded['BodyPart_Biceps'] = data_encoded['BodyPart_Biceps']
        data_encoded['BodyPart_Triceps'] = data_encoded['BodyPart_Triceps']
        data_encoded['BodyPart_Abdominals'] = data_encoded['BodyPart_Abdominals']
        data_encoded['BodyPart_FullBody'] = data_encoded[
            ['BodyPart_Legs', 'BodyPart_Back', 'BodyPart_Chest', 'BodyPart_Biceps', 'BodyPart_Triceps',
             'BodyPart_Shoulders', 'BodyPart_Abdominals']].min(axis=1)
        data_encoded.drop(
            columns=['Equipment_Cable', 'Equipment_Machine', 'Equipment_E-Z Curl Bar', 'Equipment_Barbell',
                     'Equipment_Dumbbell', 'Equipment_Body Only'], inplace=True)
        data_encoded.drop(columns=['BodyPart_Quadriceps', 'BodyPart_Hamstrings', 'BodyPart_Calves', 'BodyPart_Glutes',
                                   'BodyPart_Lats', 'BodyPart_Lower Back', 'BodyPart_Middle Back', 'BodyPart_Traps',
                                   'BodyPart_Adductors', 'BodyPart_Abductors'], inplace=True, errors='ignore')

        columns_to_drop = [
            'Type_Olympic Weightlifting', 'Type_Plyometrics', 'Type_Powerlifting', 'Type_Strongman',
            'Equipment_Bands', 'Equipment_Exercise Ball', 'Equipment_Foam Roll',
            'Equipment_Kettlebells', 'Equipment_Medicine Ball', 'Equipment_Other'
        ]
        data_encoded.drop(columns=columns_to_drop, inplace=True)

        data_encoded.iloc[:, 3:] = data_encoded.iloc[:, 3:] #.astype(int)
        self.data_encoded = data_encoded.dropna(subset=['Desc'])
        print("Successfully loaded and encoded dataset.")

    def get_recommendations(self, user_preferences, n):
        user_vector = np.array(list(user_preferences.values())).reshape(1, -1)

        cosine_similarities = []
        for i in range(len(self.data_encoded)):
            exc_vector = self.data_encoded.iloc[i, 3:].values.reshape(1, -1)
            similarity = cosine_similarity(exc_vector, user_vector)
            cosine_similarities.append(similarity[0][0])

        data_encoded_copy = self.data_encoded.copy(deep=True)
        data_encoded_copy['Cosine_Similarity'] = cosine_similarities

        data_encoded_sorted = data_encoded_copy.sort_values(by='Cosine_Similarity', ascending=False)
        recommended_exercises_with_highest_similarity = data_encoded_sorted[
            data_encoded_sorted['Cosine_Similarity'] == data_encoded_sorted['Cosine_Similarity'].max()
            ]

        shuffled_recommended_exercises = recommended_exercises_with_highest_similarity.sample(frac=1).reset_index(
            drop=True)
        top_10_recommended_exercises = shuffled_recommended_exercises.head(n)
        data = top_10_recommended_exercises.to_dict(orient='records')

        transformed_records = []
        for record in data:
            new_record = {
                'title': record['Title'],
                'desc': record['Desc'],
                'exercise_id': record['Unnamed: 0'],  # Including the 'Unnamed: 0' column value.
                'encoded_values': {key: int(value) for key, value in record.items() if
                                   key not in ['Title', 'Desc', 'Cosine_Similarity', 'Unnamed: 0']}
            }

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

    def get_recommendations_for_selected_indices(self, selected_dataset_indices, n):
        """
        Recommendations based on selected exercises.
        """
        encoded_vectors = []
        for index in selected_dataset_indices:
            record = self.data_encoded[self.data_encoded["Unnamed: 0"] == index].to_dict(orient='records')[0]
            encodings = {key: int(value) for key, value in record.items() if
                         key not in ['Title', 'Desc', 'Cosine_Similarity', 'Unnamed: 0']}
            encoded_vectors.append(encodings)

        unique_dicts = _get_unique_dicts(encoded_vectors)

        results = []
        for unique_dict in unique_dicts:
            result = self.get_recommendations(unique_dict, n)
            results.extend(result)

        return results

    def workout_details(self, dataset_index):
        record = self.data_encoded[self.data_encoded["Unnamed: 0"] == dataset_index].to_dict(orient='records')[0]
        new_record = {
            'title': record['Title'],
            'desc': record['Desc'],
            'exercise_id': record['Unnamed: 0'],  # Including the 'Unnamed: 0' column value.
            'encoded_values': {key: int(value) for key, value in record.items() if
                               key not in ['Title', 'Desc', 'Cosine_Similarity', 'Unnamed: 0']}
        }
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

        return new_record


def _get_unique_dicts(dicts):
    unique_dicts = []
    for d in dicts:
        if d not in unique_dicts:
            unique_dicts.append(d)
    return unique_dicts
