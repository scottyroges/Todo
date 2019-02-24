from flask import Flask, jsonify
from app.controller import register_controllers
from app.database import configure_database, load_models
from app.errors import AppError

# Create flask app
app = Flask(__name__)

# Setup DB
db = configure_database(app)
load_models()

# Setup routes
register_controllers(app)


# Error handler
@app.errorhandler(AppError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# include this for local dev
if __name__ == '__main__':
    print("called from main")
    app.run(debug=True)
