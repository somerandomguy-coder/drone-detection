import shutil
from pathlib import Path
from uuid import uuid4

from app.model import model
from fastapi import FastAPI, File, HTTPException, UploadFile, status

UPLOAD_FOLDER = Path("upload_images")
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = FastAPI()


@app.get("/")
def helloWorld():
    return {"message": "Hello World"}


@app.get("/checkhealth")
def checkhealth():
    return {"status": "healthy"}


# take an image, return the bounding boxes
@app.post("/predict")
async def predict(file: UploadFile = File()):
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

    save_path = Path(str(save_path) + str(uuid4()))

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output = model(save_path)
    return {"result": output}
