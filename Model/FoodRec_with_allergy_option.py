import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Load the dataset
data = pd.read_csv('recipes.csv')

# Perform data preprocessing and feature extraction
extracted_data = data[['RecipeId', 'Name', 'CookTime', 'PrepTime', 'TotalTime', 'RecipeIngredientParts',
                       'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
                       'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent', 'RecipeInstructions']]

# Create a pipeline for data preprocessing and model training
scaler = StandardScaler()
neigh = NearestNeighbors(metric='cosine', algorithm='brute')
pipeline = Pipeline([('std_scaler', scaler),
                     ('NN', neigh)])

# Fit the pipeline on the extracted data
pipeline.fit(extracted_data.iloc[:, 6:15].to_numpy())

# Define the feature names
feature_names = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
                 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']

# Function to preprocess user preferences
def preprocess_user_preferences(user_preferences, scaler):
    user_features = [user_preferences.get(feature, 0) for feature in feature_names]
    user_features_scaled = scaler.transform([user_features])
    return user_features_scaled

# Function to get recipe recommendations
def get_recommendations(user_preferences, pipeline, extracted_data, allergy_keywords, top_n=5):
    user_features_scaled = preprocess_user_preferences(user_preferences, pipeline['std_scaler'])
    _, neighbor_indices = pipeline['NN'].kneighbors(user_features_scaled, n_neighbors=top_n*2)  # Retrieve more neighbors
    recommended_recipes = extracted_data.iloc[neighbor_indices[0]]
    
    # Filter out recipes containing the allergy keywords
    if allergy_keywords:
        for keyword in allergy_keywords:
            recommended_recipes = recommended_recipes[~recommended_recipes['RecipeIngredientParts'].str.contains(keyword, case=False)]
    
    return recommended_recipes.head(top_n)

# API endpoint to get recipe recommendations
def recommend_recipes(user_preferences, allergy_keywords=None):
    if allergy_keywords is None:
        allergy_keywords = []
    else:
        allergy_keywords = [keyword.strip() for keyword in allergy_keywords.split(',')]
    
    recommendations = get_recommendations(user_preferences, pipeline, extracted_data, allergy_keywords)
    
    columns_to_print = ['Name']
    if 'RecipeCategory' in recommendations.columns:
        columns_to_print.append('RecipeCategory')
    if 'CookTime' in recommendations.columns:
        columns_to_print.append('CookTime')
    if 'PrepTime' in recommendations.columns:
        columns_to_print.append('PrepTime')
    if 'TotalTime' in recommendations.columns:
        columns_to_print.append('TotalTime')
    
    recommended_recipes = []
    for idx, recipe in recommendations[columns_to_print].iterrows():
        recipe_info = {column: recipe[column] for column in columns_to_print}
        recommended_recipes.append(recipe_info)
    
    return recommended_recipes

# Example usage
user_preferences = {
    'Calories': 500,
    'FatContent': 20,
    'SaturatedFatContent': 5,
    'CholesterolContent': 30,
    'SodiumContent': 200,
    'CarbohydrateContent': 50,
    'FiberContent': 4,
    'SugarContent': 8,
    'ProteinContent': 25
}
allergy_keywords = input("Enter your allergy keywords (comma-separated): ")

recommendations = recommend_recipes(user_preferences, allergy_keywords)
print(f"Recommended Recipes (excluding recipes with {allergy_keywords}):")
print(recommendations)
