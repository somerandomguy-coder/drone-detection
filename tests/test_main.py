import os
import sys

from fastapi.testclient import TestClient

root = os.path.abspath(os.path.dirname(".."))
sys.path.append(root)

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_checkhealth():
    response = client.get("/checkhealth")

    assert response.status_code == 200
    assert response.content == b"<div>The server is healthy</div>"


def test_predict():
    with TestClient(app) as client:
        with open("examples/Untitled.png", "rb") as f:
            fileobj = f.read()

        file_payload = ("randomfile.png", fileobj, "image/*")
        response = client.post("/predict", files={"file": file_payload})

        assert response.status_code == 200
        content = response.content

        assert isinstance(content, bytes)

        assert content[:4] == b"<svg"
        assert content[-6:] == b"</svg>"


def test_predict_empty_file():
    with TestClient(app) as client:
        fileobj = b""

        file_payload = ("randomfile.png", fileobj, "image/*")
        response = client.post("/predict", files={"file": file_payload})

        assert response.status_code == 400
        assert response.json() == {"detail": "File have to be not empty"}


def test_predict_file_too_large():
    with TestClient(app) as client:
        MAX_SIZE = (10 * 1024 * 1024) + 10
        # this actually need more memory than 10mb because python object already
        fileobj = b"*" * MAX_SIZE

        file_payload = ("randomfile.png", fileobj, "image/*")
        response = client.post("/predict", files={"file": file_payload})

        assert response.status_code == 413
        assert response.json()["detail"].startswith("File exceeded 10MB")
