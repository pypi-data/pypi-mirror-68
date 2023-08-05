import base64
import json
import os
import shutil
from pathlib import Path

import requests
from monitaur.exceptions import ClientAuthError, ClientValidationError

from monitaur.utils import (  # noqa isort:skip
    add_image,
    generate_anchors,
    get_influences,
    valid_model,
    validate_influences,
)

base_url = "https://api.monitaur.ai"


class Monitaur:
    def __init__(self, client_secret, base_url=base_url):
        self._session = requests.Session()

        self._session.headers["User-Agent"] = "monitaur-client-library"

        self.client_secret = client_secret

        self.base_url = base_url
        self.transaction_url = f"{self.base_url}/api/transactions/"
        self.models_url = f"{self.base_url}/api/models/"
        self.download_url = f"{self.base_url}/api/models"
        self.login_url = f"{self.base_url}/api/auth/?grant_type=client_credentials"

    def authenticate(self, client_secret: str) -> str:
        """
        Authenticates the user from the API
        Parameters
        ----------
        client_secret

        Returns
            access: Access token for authentication
            refresh: Refresh token to renew access
        -------

        """
        json = {"client_secret": client_secret}
        response = self._session.post(self.login_url, json=json)

        # TODO: move status_code parsing and validating to new module

        if response.status_code == requests.status_codes.codes.not_found:
            raise ClientAuthError("Invalid base URL")

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid client secret")

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request")

        return response.json()["access"]

    def add_model(
        self,
        name: str,
        model_type: str,
        model_class: str,
        library: str,
        trained_model_hash: str,
        production_file_hash: str,
        feature_number: int,
        owner: str,
        developer: str,
        version: float = 0.1,
        influences: str = None,
        counterfactual: bool = False,
    ) -> str:
        """
        Adds metadata about the machine learning model to the system.

        Args:
            name: Unique name for what this model is predicting.
            model_type: Type of model
              (linear_regression, logistic_regression, decision_tree, svm, naive_bayes, knn,
                k_means, random_forest, gmb, xgboost, lightgbm, catboost, recurrent_neural_network,
                convolutional_neural_network, generative_adversarial_network, recursive_neural_network,
                long_short_term_memory)
            model_class: This field can contain one of these values: tabular, image, nlp.
            library: Machine learning library
              (tensorflow, pytorch, apache_spark, scikit_learn, xg_boost, light_gbm,
                keras, statsmodels, caffe)
            trained_model_hash:
              Trained model file hash. Must be a joblib. None is also allowed.
            production_file_hash:
              Production file that uses the trained model for prediction.
              This should also have the logic that converts the prediction into something humanreadable.
              None is allowed.
              Example:
              ```
              def get_prediction(data_array):
                  diabetes_model = load("./_example/data.joblib")
                  data = array([data_array])
                  result = diabetes_model.predict(data)

                  prediction = "You do not have diabetes"
                  if result[0] == 1:
                      prediction = "You have diabetes"

                  return prediction
              ```
            feature_number: Number of inputs.
            owner: Name of the model owner.
            developer: Name of the data scientist.
            image: Is it an image model? Defaults to False.
            version: Monitaur model version. Defaults to 0.1.
            influences:
              Obtain decision influences.
              This field can contain one of these values: anchors, grad-cam, custom-dict, custom-image, None
            counterfactuals: Do you want to be able to perform counterfactuals?

        Returns:
            model_set_id: A UUID string for the monitaur model set.
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        if influences and influences not in [
            "anchors",
            "grad-cam",
            "custom-dict",
            "custom-image",
        ]:
            raise ClientValidationError(
                "Invalid influences. Must be either anchors, grad-cam, custom-dict, custom-image, or None"
            )

        json = {
            "name": name,
            "model_type": model_type.lower(),
            "model_class": model_class,
            "library": library.lower(),
            "trained_model_hash": trained_model_hash,
            "production_file_hash": production_file_hash,
            "feature_number": feature_number,
            "owner": owner,
            "developer": developer,
            "version": version,
            "influences": influences,
            "counterfactual": counterfactual,
        }
        response = self._session.post(self.models_url, json=json)

        print(response.status_code)
        print(response.__dict__)

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json().get("model_set_id")

    def record_training_tabular(
        self,
        model_set_id: str,
        trained_model,  # serialized model
        training_data,  # example numpy array
        feature_names: list,
        re_train: bool = False,
    ):
        """
        Sends trained model and anchors data to the API.
        Currently works only for traditional, tabular machine learning models.

        Args:
            model_set_id: A UUID string for the monitaur model set received from the API.
            trained_model: Serialized model (.joblib, .pickle).
            training_data: Training data (x training).
            feature_names: Model inputs.
            re_train: Model version will be increased by 1.0 when it is True.

        Returns:
            True
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.models_url}set/{model_set_id}/")

        model = response.json()
        version = model["version"]
        influences = model["influences"]
        model_class = model["model_class"]

        model_extension = Path(trained_model).suffix
        open(f"{model_set_id}{model_extension}", "w")
        model_filename = Path(f"{model_set_id}{model_extension}")
        shutil.copy(str(Path(trained_model)), str(model_filename))

        if not valid_model(model_extension, model_class):
            return False

        with open(model_filename, "rb") as f:
            binary = (base64.b64encode(f.read())).decode("utf-8")

        if re_train:
            version = self._increase_model_version(version, major=True)

        payload = {
            "model_set_id": model_set_id,
            "version": version,
            "model_name": f"{model_set_id}/{version}/{model_filename}",
            "model_data": binary,
        }

        if influences:
            anchor_filename, anchor_binary = generate_anchors(
                model_extension,
                model_filename,
                feature_names,
                training_data,
                model_set_id,
            )
            payload["anchor_name"] = f"{model_set_id}/{version}/{anchor_filename}"
            payload["anchor_data"] = anchor_binary

            if os.path.exists(anchor_filename):
                os.remove(anchor_filename)

        # Send Model Binary and (optional) Anchor data to api for s3 upload and update training version
        initial_data = response.json()

        response = self._session.post(
            f"{self.models_url}set/{model_set_id}/", json=payload
        )
        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", initial_data)

        print(f"Training recording: model_set_id {model_set_id}, version {version}")

        if os.path.exists(model_filename):
            os.remove(model_filename)

        return True

    def record_training_image(
        self,
        model_set_id: str,
        trained_model,  # serialized model
        re_train: bool = False,
    ):
        """
        Sends trained model to the API.

        Args:
            model_set_id: A UUID string for the monitaur model set received from the API.
            trained_model: Serialized model (.joblib, .tar, .h5).
            re_train: Model version will be increased by 1.0 when it is True.

        Returns:
            True
        """

        token = self.authenticate(self.client_secret)
        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.models_url}set/{model_set_id}/")
        model = response.json()
        version = model["version"]
        model_class = model["model_class"]

        model_extension = Path(trained_model).suffix
        open(f"{model_set_id}{model_extension}", "w")
        model_filename = Path(f"{model_set_id}{model_extension}")
        shutil.copy(str(Path(trained_model)), str(model_filename))

        if not valid_model(model_extension, model_class):
            return False

        with open(model_filename, "rb") as f:
            binary = (base64.b64encode(f.read())).decode("utf-8")

        if re_train:
            version = self._increase_model_version(version, major=True)

        # Send Model data to api for s3 upload and Update Training Version
        payload = {
            "model_set_id": model_set_id,
            "version": version,
            "model_name": f"{model_set_id}/{version}/{model_filename}",
            "model_data": binary,
        }

        initial_data = response.json()

        response = self._session.post(
            f"{self.models_url}set/{model_set_id}/", json=payload
        )
        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", initial_data)

        print(f"Training recording: model_set_id {model_set_id}, version {version}")
        return True

    def _increase_model_version(self, version, major=False):
        if isinstance(version, str):
            version = float(version)

        if major:
            return version + 1.0

        return version + 0.1

    def record_transaction(
        self,
        model_set_id: str,
        trained_model_hash: str,
        production_file_hash: str,
        prediction: str,
        features: dict = None,
        native_transaction_id: str = None,
        image: str = None,
        custom_influences: str = None,
        python_version: str = None,
        ml_library_version: str = None,
    ) -> dict:
        """
        Sends transaction details to the server.

        Args:
            model_set_id: A UUID string for the monitaur model set received from the API.
            trained_model_hash: Trained model file hash. Must be a joblib.
            production_file_hash:
              Production file that uses the trained model for prediction.
              This should also have the logic that converts the prediction into something humanreadable.
              Example:
              ```
              def get_prediction(data_array):
                  diabetes_model = load("./_example/data.joblib")
                  data = array([data_array])
                  result = diabetes_model.predict(data)

                  prediction = "You do not have diabetes"
                  if result[0] == 1:
                      prediction = "You have diabetes"

                  return prediction
              ```
            prediction: Outcome from the production prediction file.
            features: key/value pairs of the feature names and values.
            native_transaction_id: Unique identifier for the customer (optional).
            image: file path to the image to be uploaded if the model_class is an image
            custom_influences:
              Custom influences string
              model.influences must be custom in order to use this field
            python_version: Stores python version. Ensure the data follows semver - major.minor.release
            ml_library_version: Stores ML library version. Ensure the data follows semver - major.minor.release

        Returns:
            Transaction details from the server
        """
        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        response = self._session.get(f"{self.models_url}set/{model_set_id}/")
        response_data = response.json()

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response_data)

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response_data)

        version = response_data["version"]
        influences = response_data.get("influences", False)
        model_class = response_data["model_class"]

        valid = validate_influences(influences, model_class, custom_influences)

        if influences in ["custom-dict", "custom-image"] and valid:
            if influences == "custom-dict":
                influences = json.dumps(custom_influences)
            else:
                influences = add_image(custom_influences)

        if "model_class" in response_data and model_class == "image":
            if image is None:
                raise ClientValidationError("No Image")

        if "model_class" in response_data and model_class != "image":
            if features is None:
                raise ClientValidationError("Features is required")

        transaction_data = {
            "model": model_set_id,
            "trained_model_hash": trained_model_hash,
            "production_file_hash": production_file_hash,
            "prediction": prediction,
            "influences": influences,
            "native_transaction_id": native_transaction_id,
            "python_version": python_version,
            "ml_library_version": ml_library_version,
        }

        if features is not None:
            transaction_data["features"] = features

        if influences == "anchors" and image is None:
            download_response = self._session.get(
                f"{self.models_url}download/{model_set_id}/{version}"
            )
            data = download_response.json()
            if (
                download_response.status_code
                == requests.status_codes.codes.unauthorized
            ):
                raise ClientAuthError("Invalid token", data)

            if download_response.status_code == requests.status_codes.codes.bad_request:
                raise ClientValidationError("Bad Request", data)

            influences = get_influences(data, model_set_id, features)
            transaction_data.update({"influences": json.dumps(influences)})

            if os.path.exists(f"{model_set_id}.anchors"):
                os.remove(f"{model_set_id}.anchors")

        if image is not None:
            image_byte = add_image(image)
            transaction_data.update({"image": image_byte})
            transaction_data.update({"image_influences": influences})

        response = self._session.post(self.transaction_url, json=transaction_data,)

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json()

    def read_transactions(self, model_id: int = None, model_set_id: str = None) -> list:
        """
        Retrieves transactions.

        Args:
            model_id: An int for the monitaur model received from the API. (optional)
            model_set_id: A UUID string for the monitaur model set received from the API. (optional)

        Returns:
            List of transactions
        """

        token = self.authenticate(self.client_secret)

        self._session.headers["Authorization"] = f"Token {token}"

        querystring = {}
        if model_id:
            querystring.update({"model": model_id})
        if model_set_id:
            querystring.update({"model_set_id": model_set_id})

        response = self._session.get(self.transaction_url, params=querystring)

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise ClientAuthError("Invalid token", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ClientValidationError("Bad Request", response.json())

        return response.json()
