from flask import Flask, render_template
from flask_cors import CORS
from config.app_config import AppConfig
from routes.home import configure_home_routes
from routes.alphabets_quiz import configure_alphabets_routes
from routes.words_quiz import configure_words_routes

app = Flask(__name__)

config = AppConfig()


app.config.from_object(config)
# Set a secret key
app.secret_key = "daignosing-ai-assisstant"
# Enable CORS for all routes
CORS(app)

# Register home routes
configure_home_routes(app)

# Register alphabets routes
configure_alphabets_routes(app)

# Register words routes
configure_words_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host=config.HOST, port=config.PORT)
