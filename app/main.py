import asyncio
import shutil
from pathlib import Path
from uuid import uuid4

from app.aimodel import get_yolo, model
from app.database import initialize_database, save_prediction
from fastapi import FastAPI, File, HTTPException, UploadFile, status

UPLOAD_FOLDER = Path("upload_images")
UPLOAD_FOLDER.mkdir(exist_ok=True)


app = FastAPI()

# initialize here so the yolo object stay alive the whole lifetime of the application
yolo_model = get_yolo()
asyncio.run(initialize_database())


@app.get("/")
async def helloWorld():
    return {"message": "Hello World"}


@app.get("/checkhealth")
async def checkhealth():
    return {"status": "healthy"}


# Take an image, return the bounding boxes
@app.post("/predict/{id}")
async def predict(id: str, file: UploadFile = File()):
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
    output = await model(yolo_model, save_path)

    await save_prediction(id, save_path, output)
    return {"result": output}
