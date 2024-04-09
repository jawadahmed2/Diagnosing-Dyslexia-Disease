from flask import Blueprint, request, send_from_directory, render_template
import os
import uuid
import numpy as np
import base64
from PIL import Image
import io

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
            img_data, os.path.join(alphabets_routes.config["UPLOAD_FOLDER"], filename)
        )

        return "Image saved successfully"


@alphabets_routes.route("/images/input/alphabets/<filename>")
def uploaded_file(filename):
    return send_from_directory(alphabets_routes.config["UPLOAD_FOLDER"], filename)


# Function to save the image from data using Pillow
def save_image_from_data(img_data, filename):
    # Decode the base64 image data and convert it to a Pillow image
    img_bytes = base64.b64decode(img_data)
    img_pil = Image.open(io.BytesIO(img_bytes))

    # Invert the colors of the image
    inverted_img_pil = Image.eval(img_pil, lambda x: 255 - x)

    # Save the inverted image
    inverted_img_pil.save(filename)


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
