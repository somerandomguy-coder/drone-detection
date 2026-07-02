# 🛸 Drone Detection Web Application

> An asynchronous full-stack web application that detects drones in uploaded images using a fine-tuned YOLOv8 model and displays real-time SVG bounding box overlays.

## 📷 Preview

| 1. Upload & Preview | 2. Detection Result (SVG Overlay) |
| :---: | :---: |
| <img src="frontend/asset/before.png" width="400" alt="Upload Screen"> | <img src="frontend/asset/after.png" width="400" alt="Result Screen"> |

---

## 🚀 Features

* **AI-Powered Detection:** Leverages Ultralytics YOLOv8 object detection framework via OpenCV.
* **Asynchronous Backend:** Powered by FastAPI for high-performance, non-blocking I/O operations.
* **Dynamic UI Overlay:** The JavaScript frontend translates prediction coordinates directly into an absolutely positioned SVG overlay drawn cleanly over the source image.
* **Robust Validation:** Safeguards against empty file submissions and strict file size limits ($< \text{10 MB}$).
* **Stateless & Containerized:** Completely stateless container design, built for seamless serverless deployment and horizontal scaling.
* **Automated Testing:** Test suite covering endpoints, validation limits, and edge-case exceptions using `pytest`.

---

## 📁 Project Structure

```text
.
├── app/
│   ├── aimodel.py        # YOLOv8 configuration and prediction engine
│   └── main.py           # FastAPI server routing, CORS, and SVG generator
├── examples/             # Sample images for testing or showcasing
│   ├── cars-city-traffic-daylight_23-2149092081.avif
│   └── Untitled.png
├── frontend/             # Frontend client assets
│   ├── asset/
│   │   └── Drones 1600x800.webp
│   ├── css/
│   │   └── style.css
│   ├── index.html
│   └── scripts/
│       └── index.js
├── models/               # Model weights storage
│   └── best.pt           # Fine-tuned YOLOv8 weights (drone detector)
├── notebooks/            # Jupyter notebooks used during EDA/Training
│   └── notebook094b2d999a.ipynb
├── tests/                # Automated test cases
│   └── test_main.py
├── firebase.json         # Firebase Hosting deployment config
├── TODO.md               # Practice task list for hand-coded improvements
├── .env                  # Configuration environment variables
└── requirements.txt      # Python package dependencies
```

---

## 🛠️ Setup and Installation

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your machine.

### 2. Environment Configuration

Open your terminal in the project root directory and create a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all required third-party libraries:

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables (`.env`)

Create a `.env` file in the root directory to customize your local defaults:

```ini
model_path="models/best.pt"
save_output=False
confidence=0.5
image_size=640
```

---

## 🖥️ Running the Application

### Start the Backend Server

Fire up the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --port 8080 --reload
```

Upon startup, the server will load the configured YOLO model and serve on `http://127.0.0.1:8080`.

### Launch the Frontend

Because the backend includes full CORS access (`allow_origins=["*"]`), you can simply open the `frontend/index.html` file directly in any modern web browser to interact with the system.

1. **Select an image** to instantly see a preview.
2. Click **Submit** to process the image through the YOLO backend.
3. Watch the SVG overlay generate automatically over the target drone!

---

## 🌐 Production Deployment

The project is designed to be fully serverless:

### Backend: Google Cloud Run
- Containerized using the included `Dockerfile`.
- Run on Google Cloud Run in a serverless environment.
- Configured with `2 GiB` Memory and `2 CPU` to support fast deep-learning inference speeds.

### Frontend: Firebase Hosting
- Configured via `firebase.json`.
- Served over a globally distributed CDN with automatic HTTPS.
- Deployed via the Firebase CLI:
  ```bash
  firebase deploy --project <PROJECT_ID> --only hosting
  ```

---

## 🧪 Running Tests

The test suite includes validation tests for server responses, bounding boxes formatting, empty uploads, and file-size exception blocks.

Run your test files using `pytest`:

```bash
pytest tests/
```

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Response Type | Description |
| --- | --- | --- | --- |
| `/` | `GET` | `application/json` | Base health indicator greeting. |
| `/checkhealth` | `GET` | `text/html` | Standard status ping (`The server is healthy`). |
| `/predict` | `POST` | `text/html` | Receives multipart form image data, runs object detection, and returns custom SVG elements containing coordinates and confidence rates. |
