from flask import Flask, jsonify
from app.controller import register_controllers
from app.database import configure_database
from app.errors import AppError
from app.model import load_models, load_schemas

app = Flask(__name__)

db = configure_database(app)

load_models()
load_schemas(db)
register_controllers(app)


@app.errorhandler(AppError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# include this for local dev
if __name__ == '__main__':
    app.run(debug=True)
