from io import BytesIO

import joblib
import pytest
from monitaur import hash_file
from monitaur.exceptions import CustomInfluencesError, FileError
from monitaur.utils import generate_anchors, valid_model, validate_influences
from monitaur.virgil.alibi.tabular import AnchorTabular


def test_hash_file_returns_sha256_hash_of_a_file(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value = BytesIO(b"12345")

    result = hash_file("filename")

    mock_open.assert_called_once_with("filename", "rb")
    assert result == "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"


def test_valid_model():
    assert valid_model(".pickle", "tabular")
    assert valid_model(".h5", "image")

    with pytest.raises(FileError) as excinfo:
        valid_model(".h5", "tabular")
    assert (
        "Invalid model. Acceptable files: '.joblib', '.pickle'."
        == excinfo.value.message
    )

    with pytest.raises(FileError) as excinfo:
        valid_model("", "image")
    assert (
        "Invalid model. Acceptable files: '.joblib', '.tar', '.h5'."
        == excinfo.value.message
    )


def test_generate_anchors(mocker, training_data):
    mocker.patch.object(
        joblib, "load", return_value=b"Image-Base-64-encoded-return-data"
    )
    mocker.patch.object(AnchorTabular, "__init__", return_value=None)
    mocker.patch.object(AnchorTabular, "fit")

    assert generate_anchors(
        ".joblib",
        "job.joblib",
        [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeF",
            "Age",
        ],
        training_data,
        1,
    )


@pytest.mark.parametrize(
    "model_influences, model_class, custom_influences",
    [
        ("custom-dict", "tabular", {}),
        ("custom-image", "tabular", "foo.png"),
        ("anchors", "tabular", None),
        ("grad-cam", "tabular", None),
        (None, "tabular", None),
        ("custom-dict", "image", {}),
        ("custom-image", "image", "foo.png"),
        ("anchors", "image", None),
        ("grad-cam", "image", None),
        (None, "image", None),
        ("custom-dict", "nlp", {}),
        ("custom-image", "nlp", "foo.png"),
        ("anchors", "nlp", None),
        ("grad-cam", "nlp", None),
        (None, "nlp", None),
    ],
)
def test_validate_influences_valid(model_influences, model_class, custom_influences):
    assert validate_influences(model_influences, model_class, custom_influences)


@pytest.mark.parametrize(
    "model_influences, model_class, custom_influences, value",
    [
        ("custom-dict", "tabular", "foo.png", "a dict"),
        ("custom-image", "tabular", {}, "a string file path"),
        ("anchors", "tabular", {}, "None"),
        ("grad-cam", "tabular", {}, "None"),
        (None, "tabular", {}, "None"),
        ("custom-dict", "image", "foo.png", "a dict"),
        ("custom-image", "image", {}, "a string file path"),
        ("anchors", "image", {}, "None"),
        ("grad-cam", "image", {}, "None"),
        (None, "image", {}, "None"),
        ("custom-dict", "nlp", "foo.png", "a dict"),
        ("custom-image", "nlp", {}, "a string file path"),
        ("anchors", "nlp", {}, "None"),
        ("grad-cam", "nlp", {}, "None"),
        (None, "nlp", {}, "None"),
    ],
)
def test_validate_influences_invalid(
    model_influences, model_class, custom_influences, value
):
    with pytest.raises(CustomInfluencesError) as excinfo:
        validate_influences(model_influences, model_class, custom_influences)
    assert (
        f"When model.influences is {model_influences}, custom_influences must be {value}"
        == excinfo.value.message
    )
