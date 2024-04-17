from flask import Blueprint, request, send_from_directory, render_template, jsonify
import os
import uuid
import numpy as np
import base64
from PIL import Image
import io
from model.load_model import LoadModel

deep_learning_model = LoadModel()

words_result = {}
overall_result = {}
piechart_data = {}

words_routes = Blueprint("words_routes", __name__)

UPLOAD_FOLDER = "static/images/input/words"
words_routes.config = dict()
words_routes.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@words_routes.route("/words")
def main_page():
    # Reset dictionaries when the page is reloaded
    words_result.clear()
    overall_result.clear()
    piechart_data.clear()
    return render_template("words.html")


@words_routes.route("/upload-words", methods=["POST"])
def upload_words():
    if request.method == "POST":
        # Get the image data from the POST request
        img_data = request.form["img_data"]
        letter_number = request.form["letter_number"]

        # Decode the image data
        img_data = img_data.split(",")[1]

        # Generate a unique filename for each image
        filename = str(uuid.uuid4()) + ".png"

        # Save the image to the designated folder using Pillow
        save_image_from_data(
            img_data, os.path.join(
                words_routes.config["UPLOAD_FOLDER"], filename), letter_number
        )

        return "Image saved successfully"


@words_routes.route("/images/input/words/<filename>")
def uploaded_file(filename):
    return send_from_directory(words_routes.config["UPLOAD_FOLDER"], filename)


@words_routes.route("/word-result", methods=["GET"])
def get_result():
    # Check if there are any records in words_result
    if not words_result:
        return jsonify({"error": "No results available"})

    # Get the last record from words_result
    last_filename = list(words_result.keys())[-1]
    last_record = words_result[last_filename]

    # Extract label and score from the last record
    label = last_record["label"]
    score = last_record["score"]

    # Return label and score in JSON format
    return jsonify({"label": label, "score": score})


@words_routes.route("/overall-word-result", methods=["GET"])
def get_overall_result():
    overall_score = 0

    # Calculate the overall score by summing up all the scores
    for record in words_result.values():
        overall_score += record["score"]

    # Calculate the predicted result based on the overall score
    if overall_score >= 45:
        predicted_result = "Hurrah! There is no Dyslexia Found"
    else:
        predicted_result = "Alas! There is dyslexia"

    # Return the predicted result and overall score in JSON format
    return jsonify({"Prediction": predicted_result, "overall_score": overall_score})


@words_routes.route("/word-piechart-data", methods=["GET"])
def get_piechart_data():
    # Dictionary to store the count of each label
    label_counts = {"Normal": 0, "Correlated": 0, "Reversal": 0}

    # Iterate over the words_result dictionary to count occurrences of each label
    for result in words_result.values():
        label = result["label"]
        if label in label_counts:
            label_counts[label] += 1

    # Prepare data for pie chart
    piechart_data = [{"label": label, "count": count}
                     for label, count in label_counts.items()]

    return jsonify(piechart_data)


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


def save_image_from_data(img_data, filename, letter_number):
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

    # Store the accuracy and label_index in the words_result dictionary
    words_result[letter_number] = {
        "label": label,
        "accuracy": float(accuracy),
        "score": score
    }

# Function to configure home routes in the Flask app


def configure_words_routes(app):
    """
    Configure and register home-related routes with a Flask app.

    Args:
    - app: Flask app instance.

    Returns:
    - auth_routes: Blueprint for home-related routes.
    """
    app.register_blueprint(words_routes)
    return words_routes
