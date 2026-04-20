from flask import Flask
from flask_cors import CORS
from routes.match import match_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(match_bp)

if __name__ == '__main__':
    app.run(debug=True)