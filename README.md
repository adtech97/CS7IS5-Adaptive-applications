# CS7IS5-Adaptive-applications

### Current setup
1. API server which lets you:
   * Sign Up
   * Login
   * Log exercise entries
   * Log foods entries
   * View exercise history
   * View food history
2. Local SQLite DB so we don't have to worry about setting up Postgres for now.

### Running the API server
1. Setup local environment and install required PIP packages: `pip install -r requirements.txt`
2. Run the server `python start_api_server.py`
3. Testing:
   * Load postman collection `adaptive.postman_collection.json` in your Postman application.
   * Run queries, note that JWT token gets generated using `/login` and needs to be included under `Authorization -> Bearer Token`.