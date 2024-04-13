import numpy as np
from PIL import Image
from numpy import loadtxt
from keras.models import load_model
import numpy as np
import cv2
import pickle
import os


class LoadModel:
    # def __init__(self) -> None:
    #     main_dir = os.path.dirname(os.path.abspath(__file__))
    #     model_path = os.path.join(main_dir, 'ensemble_model_weights.pkl')
    #     # Check if the files exist
    #     if not os.path.exists(model_path):
    #         raise FileNotFoundError(f"Model file '{model_path}' not found.")
    #     # Load the saved ensemble model
    #     with open(model_path, 'rb') as f:
    #         self.model = pickle.load(f)

    # def predictImage(self, image):
    #     if not os.path.exists(image):
    #         raise FileNotFoundError(f"Image file '{image}' not found.")
    #     pic = cv2.imread(image, 0)
    #     if pic is None:
    #         raise FileNotFoundError(f"Unable to open or read image file '{image}'.")
    #     if pic.size == 0:
    #         raise ValueError(f"Image file '{image}' has size 0.")
    #     img = cv2.resize(pic, (112, 112))
    #     img_flat = img.flatten().astype('float32') / 255.0
    #     predicted_class = self.model.predict(img_flat.reshape(1, -1))
    #     if predicted_class == 0:
    #         return 'Normal', predicted_class
    #     elif predicted_class == 1:
    #         return "Correlated", predicted_class
    #     elif predicted_class == 2:
    #         return "Reversal", predicted_class

    # def user_input(self, filename):
    #     result = self.predictImage(filename)
    #     return result

    def __init__(self) -> None:
        # Get the absolute path of the directory containing the main file
        main_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute paths to the model and history files
        model_path = os.path.join(main_dir, 'best_model.h5')
        history_path = os.path.join(main_dir, 'my_history.npy')

        # Check if the files exist
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found.")
        if not os.path.exists(history_path):
            raise FileNotFoundError(
                f"History file '{history_path}' not found.")

        # Load the model and history
        self.model = load_model(model_path)
        self.history = np.load(history_path, allow_pickle=True).item()

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
        # Add an extra dimension for the grayscale channel
        X = np.expand_dims(X, axis=-1)

        # Normalize the image data
        X = X.astype('float32') / 255.0

        # Make predictions
        val = self.model.predict(X)
        val = list(val[0])
        mx = max(val)
        accuracy = f"{mx * 100:.2f}"
        # print(f'Accuracy is {accuracy}%')
        label_index = val.index(mx)
        # print(f'Label Index is {label_index}')
        label_index = int(label_index)
        if label_index == 0:
            return "Normal", accuracy, label_index
        elif label_index == 1:
            return "Correlated", accuracy, label_index
        elif label_index == 2:
            return "Reversal", accuracy, label_index

    def user_input(self, image_path):
        # Load the original image using OpenCV
        original_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        # Create a black background image with the same dimensions as the original image
        new_image = np.zeros_like(original_image)

        # Calculate the position to paste the resized image
        x_offset = (new_image.shape[1] - original_image.shape[1]) // 2
        y_offset = (new_image.shape[0] - original_image.shape[0]) // 2

        # Resize the original image to match the dimensions of the new_image
        resized_original_image = cv2.resize(
            original_image, (new_image.shape[1], new_image.shape[0]))

        # Paste the resized image onto the black background
        new_image[y_offset:y_offset+resized_original_image.shape[0],
                  x_offset:x_offset+resized_original_image.shape[1]] = resized_original_image

        print(f'Image Shape: {new_image.shape}')

        result = self.predictImage(new_image)

        return result


# if __name__ == "__main__":
#     model_load = LoadModel()
#     try:
#         print(model_load.user_input("imresizer-1711647452478.png"))
#     except FileNotFoundError as e:
#         print(e)
#     except ValueError as e:
#         print(e)
#     except Exception as e:
#         print("An error occurred:", e)
