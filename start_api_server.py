import uvicorn
from api.api import app
from database.db import  init_db


if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8080)