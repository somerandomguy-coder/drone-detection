import numpy as np
import yaml
from fastapi import FastAPI

app = FastAPI()


def model(image):
    shape = image.shape
    return [shape, 1, 2, 3, 4]


@app.get("/")
def helloWorld():
    return {"message": "Hello World"}


@app.get("/checkhealth")
def checkhealth():
    return {"status": "healthy"}


@app.post("/predict")
def predict(input):
    output = model(input)
    return {"result": output}
