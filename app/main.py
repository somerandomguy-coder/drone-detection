import json
import shutil
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.aimodel import get_yolo, model
from app.database import initialize_database, save_prediction

UPLOAD_FOLDER = Path("upload_images")
UPLOAD_FOLDER.mkdir(exist_ok=True)

MAX_SIZE = 10 * 1024 * 1024


# startup script to initialize_database
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("loading model")
    app.state.yolo_model = get_yolo()
    print("initializing database")
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


# Allow your frontend to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, swap "*" for your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# initialize here so the yolo object stay alive the whole lifetime of the application


@app.get("/")
async def helloWorld():
    return {"message": "Hello World"}


@app.get("/checkhealth", response_class=HTMLResponse)
async def checkhealth():
    return "<div>The server is healthy</div>"


# Take an image, return the bounding boxes
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File()):
    id = str(uuid4())
    file_size = file.size

    if file_size and file_size > MAX_SIZE:
        raise HTTPException(
            status.HTTP_413_CONTENT_TOO_LARGE,
            f"File exceeded 10MB, your file size was {file_size}",
        )

    if file_size == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File have to be not empty")

    filename = file.filename
    if filename is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "file have to have name")

    save_path = UPLOAD_FOLDER / filename
    save_path = Path(str(save_path) + str(uuid4()) + ".jpg")

    contents = await file.read()
    with open(save_path, "wb") as buffer:
        buffer.write(contents)

    # everytime see something could go take a while, await it
    yolo_model = request.app.state.yolo_model
    raw_output = await model(yolo_model, save_path)
    output = json.dumps(raw_output)

    await save_prediction(id, str(save_path), output)

    response = ""

    response = '<svg id="swappable_ui" class="boundingbox">' + response

    for prediction in raw_output:
        coordinate = prediction["coordinate"]
        confidence = prediction["confidence"]

        width = int(coordinate[2])
        height = int(coordinate[3])

        x_min = int(coordinate[0] - width / 2)
        y_min = int(coordinate[1] - height / 2)

        response = (
            response
            + f'<rect x="{x_min}" y="{y_min}" width="{width}" height="{height}" fill="none" stroke="red" />'
        )

        response = (
            response
            + f'<text x="{x_min}" y="{y_min + height}" fill="white">{confidence:.2f}</text>'
        )

    response = response + "</svg>"
    return response
