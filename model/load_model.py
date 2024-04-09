import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from numpy import loadtxt
from keras.models import load_model
import numpy as np
import numpy as np
import cv2


class LoadModel:
    def __init__(self) -> None:
        self.model = load_model('best_model.h5')
        self.history=np.load('my_history.npy',allow_pickle='TRUE').item()

    # Function to make predictions
    def predictImage(self, image):
        # Convert NumPy array to PIL Image
        original_image = Image.fromarray(image)

        # Resize the image while preserving the text
        img = original_image.resize((112, 112))

        # Convert the image to grayscale
        img_gray = img.convert('L')

        # Prepare the image for prediction
        X = np.array(img_gray)
        X = np.expand_dims(X, axis=0)
        X = np.expand_dims(X, axis=-1)  # Add an extra dimension for the grayscale channel

        # Normalize the image data
        X = X.astype('float32') / 255.0

        # Make predictions
        val = self.model.predict(X)
        val = list(val[0])
        mx = max(val)
        print(f'{mx*100:.2f}% Accurate')
        label_index = val.index(mx)
        print(f'Label Index is {label_index}')
        if label_index == 0:
            return "Normal"
        elif label_index == 1:
            return "Correlated"
        elif label_index == 2:
            return "Reversal"

    def user_input(self, image_path):
        # Load the original image using OpenCV
        original_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Create a black background image
        new_image = np.zeros((28, 28, 4), dtype=np.uint8)

        # Calculate the position to paste the resized image
        x_offset = (new_image.shape[1] - original_image.shape[1]) // 2
        y_offset = (new_image.shape[0] - original_image.shape[0]) // 2

        # Paste the resized image onto the black background
        new_image[y_offset:y_offset+original_image.shape[0], x_offset:x_offset+original_image.shape[1]] = original_image

        # Invert the colors (to make background black and text white)
        inverted_image = cv2.bitwise_not(cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY))

        print(f'Image Shape: {inverted_image.shape}')

        result = self.predictImage(inverted_image)

        return result

model_load = LoadModel()
print(model_load.user_input("imresizer-1711647452478.png"))