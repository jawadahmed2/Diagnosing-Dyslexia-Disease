from flask import Blueprint, jsonify, request, send_from_directory, render_template
import os
import uuid
import numpy as np
import base64
from PIL import Image
import io
from model.load_model import LoadModel

deep_learning_model = LoadModel()

alphabets_result = {}


alphabets_routes = Blueprint("alphabets_routes", __name__)

UPLOAD_FOLDER = "static/images/input/alphabets"
alphabets_routes.config = dict()
alphabets_routes.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@alphabets_routes.route("/alphabets")
def main_page():
    return render_template("alphabetical.html")


@alphabets_routes.route("/upload-alphabets", methods=["POST"])
def upload_alphabets():
    if request.method == "POST":
        # Get the image data from the POST request
        img_data = request.form["img_data"]

        # Decode the image data
        img_data = img_data.split(",")[1]

        # Generate a unique filename for each image
        filename = str(uuid.uuid4()) + ".png"

        # Save the image to the designated folder using Pillow
        save_image_from_data(
            img_data, os.path.join(
                alphabets_routes.config["UPLOAD_FOLDER"], filename)
        )

        return "Image saved successfully"


@alphabets_routes.route("/images/input/alphabets/<filename>")
def uploaded_file(filename):
    return send_from_directory(alphabets_routes.config["UPLOAD_FOLDER"], filename)


@alphabets_routes.route("/alphabet-result", methods=["GET"])
def get_result():
    # Check if there are any records in alphabets_result
    if not alphabets_result:
        return jsonify({"error": "No results available"})

    # Get the last record from alphabets_result
    last_filename = list(alphabets_result.keys())[-1]
    last_record = alphabets_result[last_filename]

    # Extract label and score from the last record
    label = last_record["label"]
    score = last_record["score"]

    # Return label and score in JSON format
    return jsonify({"label": label, "score": score})


def calculate_score(accuracy, label_index):
    score = 0
    accuracy = float(accuracy)
    if label_index == 0:
        if accuracy >= 90:
            score = 10
        elif accuracy >= 80:
            score = 9
        elif accuracy >= 70:
            score = 8
        elif accuracy >= 60:
            score = 7.5
        elif accuracy >= 50:
            score = 7
        elif accuracy >= 40:
            score = 6.5
        elif accuracy >= 30:
            score = 6.5
        elif accuracy >= 20:
            score = 6.5
        elif accuracy >= 10:
            score = 6
        else:
            score = 6
    elif label_index == 1:
        if accuracy >= 90:
            score = 6.5
        elif accuracy >= 80:
            score = 6.5
        elif accuracy >= 70:
            score = 6
        elif accuracy >= 60:
            score = 6
        elif accuracy >= 50:
            score = 5.5
        elif accuracy >= 40:
            score = 5.5
        elif accuracy >= 30:
            score = 5
        elif accuracy >= 20:
            score = 5
        elif accuracy >= 10:
            score = 4
        else:
            score = 5
    elif label_index == 2:
        if accuracy >= 90:
            score = 1
        elif accuracy >= 80:
            score = 1
        elif accuracy >= 70:
            score = 2
        elif accuracy >= 60:
            score = 2.5
        elif accuracy >= 50:
            score = 3
        elif accuracy >= 40:
            score = 3
        elif accuracy >= 30:
            score = 3.5
        elif accuracy >= 20:
            score = 4
        elif accuracy >= 10:
            score = 5
        else:
            score = 5
    return score

# Function to save the image from data using Pillow


def save_image_from_data(img_data, filename):
    # Decode the base64 image data and convert it to a Pillow image
    img_bytes = base64.b64decode(img_data)
    img_pil = Image.open(io.BytesIO(img_bytes))

    # Invert the colors of the image
    inverted_img_pil = Image.eval(img_pil, lambda x: 255 - x)
    # Save the inverted image
    inverted_img_pil.save(filename)

    label, accuracy, label_index = deep_learning_model.user_input(
        filename)

    score = calculate_score(accuracy, label_index)

    # Store the accuracy and label_index in the alphabets_result dictionary
    alphabets_result[filename] = {
        "label": label,
        "accuracy": float(accuracy),
        "score": score
    }


# Function to configure home routes in the Flask app
def configure_alphabets_routes(app):
    """
    Configure and register home-related routes with a Flask app.

    Args:
    - app: Flask app instance.

    Returns:
    - auth_routes: Blueprint for home-related routes.
    """
    app.register_blueprint(alphabets_routes)
    return alphabets_routes
