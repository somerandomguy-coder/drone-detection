import json
import shutil
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from app.aimodel import get_yolo, model
from app.database import initialize_database, save_prediction
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status

UPLOAD_FOLDER = Path("upload_images")
UPLOAD_FOLDER.mkdir(exist_ok=True)


# startup script to initialize_database
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("loading model")
    app.state.yolo_model = get_yolo()
    print("initializing database")
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


# initialize here so the yolo object stay alive the whole lifetime of the application


@app.get("/")
async def helloWorld():
    return {"message": "Hello World"}


@app.get("/checkhealth")
async def checkhealth():
    return {"status": "healthy"}


# Take an image, return the bounding boxes
@app.post("/predict/{id}")
async def predict(id: str, request: Request, file: UploadFile = File()):
    if id == "":
        id = str(uuid4())

    if file == File():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "u have to send something real"
        )

    filename = file.filename
    if filename is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "u have to send something real"
        )

    save_path = UPLOAD_FOLDER / filename
    save_path = Path(str(save_path) + str(uuid4()) + ".jpg")

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # everytime see something could go take a while, await it
    yolo_model = request.app.state.yolo_model
    output = await model(yolo_model, save_path)
    output = json.dumps(output)

    await save_prediction(id, str(save_path), output)
    return {"result": output}
