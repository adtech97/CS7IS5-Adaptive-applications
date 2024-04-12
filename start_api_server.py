import uvicorn
from api.api import app
from database.db import  init_db
from Model.workout_recommendations import WorkoutRecommendations
from Model.food_recommendations import FoodRecipeRecommendations


if __name__ == "__main__":
    init_db()
    app.state.workout_recommender = WorkoutRecommendations("Data/megaGymDataset.csv")
    app.state.food_recipe_recommender = FoodRecipeRecommendations("Data/recipes.csv")
    uvicorn.run(app, host="127.0.0.1", port=8080)
