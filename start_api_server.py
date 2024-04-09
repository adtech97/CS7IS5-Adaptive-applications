import uvicorn
from api.api import app
from database.db import  init_db
from Model.workout_recommendations import WorkoutRecommendations


if __name__ == "__main__":
    init_db()
    app.state.workout_recommender = WorkoutRecommendations("Data/megaGymDataset.csv")
    uvicorn.run(app, host="127.0.0.1", port=8080)