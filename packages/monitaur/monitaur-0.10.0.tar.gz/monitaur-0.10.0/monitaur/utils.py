import base64
import hashlib
import os
import pickle

import dill
import joblib
import numpy as np
from monitaur.virgil.alibi.tabular import AnchorTabular

from monitaur.exceptions import (  # noqa isort:skip
    ClientValidationError,
    CustomInfluencesError,
    FileError,
)


def hash_file(filename):
    hash_ = hashlib.sha256()

    with open(filename, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            hash_.update(chunk)

    return hash_.hexdigest()


def get_influences(anchor_binary_data, model_set, features):
    """
    Downloads trained model and respective influences from s3.
    Then calculates influences for a given transaction.

    Args:
        model_set: A UUID string for the monitaur model set.
        response: Json dumped anchor data from the API

    Returns:
        dict of influences
    """

    influence_threshold = 0.95

    # write explainers for the model to anchors file
    anchors_filename = f"{model_set}.anchors"
    anchor_data = base64.b64decode(anchor_binary_data["data"])

    with open(anchors_filename, "wb") as f:
        f.write(anchor_data)

    # load explainer from s3 download
    with open(anchors_filename, "rb") as f:
        explainer = dill.load(f)

    # determine influences for transaction
    inputs = list(features.values())
    reshaped_inputs = np.asarray(inputs).reshape(1, len(inputs))
    influences = explainer.explain(reshaped_inputs, threshold=influence_threshold)

    return influences["names"]


def valid_model(extension, model_class):
    """
    Validates a trained model based on the model_class.

    Args:
        extension: File extension for the serialized model (.joblib, .pickle, '.tar', '.h5).
        model_class: 'tabular' or 'image'.

    Returns:
        True if valid
    """

    if model_class == "tabular" and extension not in [".joblib", ".pickle"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.pickle'.")
    if model_class == "image" and extension not in [".joblib", ".tar", ".h5"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.tar', '.h5'.")

    return True


def generate_anchors(
    extension, trained_model, feature_names, training_data, model_set_id
):
    """
    Generates anchor

    Args:
        extension: File extension for the serialized model (.joblib, .pickle, '.tar', '.h5).
        trained_model: Instantiated model (.joblib, .pickle, '.tar', '.h5).
        feature_names: Model inputs.
        training_data: Training data (x training).
        model_set_id: A UUID string for the monitaur model set received from the API.

    Returns:
        binary
    """

    if extension == ".joblib":
        trained_model_file = joblib.load(trained_model)
    else:
        trained_model_file = pickle.load(trained_model)

    predict_fn = lambda x: trained_model_file.predict_proba(x)  # NOQA
    explainer = AnchorTabular(predict_fn, feature_names)
    explainer.fit(training_data)

    filename_anchors = f"{model_set_id}.anchors"

    with open(filename_anchors, "wb") as f:
        dill.dump(explainer, f)

    with open(filename_anchors, "rb") as f:
        return (filename_anchors, (base64.b64encode(f.read())).decode("utf-8"))


def add_image(image):
    if not os.path.exists(image):
        raise ClientValidationError("Image File path not valid")

    # Check the file extension
    extension = os.path.splitext(image)[-1].lower()
    if extension not in (".png", ".jpg", ".jpeg"):
        raise ClientValidationError("Invalid Image provided")

    file_size = float(os.path.getsize(image)) / (1024.0 ** 2)
    if file_size > 1:
        raise ClientValidationError(
            "Image Size greater than One (1) Megabyte. Choose a file with a lesser size"
        )

    with open(image, "rb") as img:
        image_byte = (base64.b64encode(img.read())).decode("utf-8")

    return image_byte


def validate_influences(model_influences, model_class, custom_influences):
    if model_influences == "custom-dict":
        if not isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is custom-dict, custom_influences must be a dict"
            )
    if model_influences == "custom-image":
        if not isinstance(custom_influences, str):
            raise CustomInfluencesError(
                "When model.influences is custom-image, custom_influences must be a string file path"
            )
    if model_influences == "anchors":
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is anchors, custom_influences must be None"
            )
    if model_influences == "grad-cam":
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is grad-cam, custom_influences must be None"
            )
    if not model_influences:
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is None, custom_influences must be None"
            )

    return True
