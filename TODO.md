# 📝 Suggested Codebase Improvements (For Self-Learning)

This TODO list contains ideas for hand-written code improvements you can implement to learn and refine your backend, container, and API design skills.

---

## 🧹 1. Ephemeral File Clean-up
* **Problem:** Currently, `/predict` saves uploaded images to the `upload_images/` directory on disk. On GCP Cloud Run, the filesystem is in-memory, so accumulating images will eventually exhaust the container's memory (causing crash loops).
* **Improvement Task:** 
  - [ ] Implement a clean-up mechanism (e.g., using a FastAPI `BackgroundTasks` to delete the saved image after prediction is complete, or using Python's `tempfile` module so files are automatically cleaned up when closed).
  - *Hint:*
    ```python
    from fastapi import BackgroundTasks

    def remove_file(path: str):
        import os
        if os.path.exists(path):
            os.remove(path)

    # In predict endpoint:
    background_tasks.add_task(remove_file, str(save_path))
    ```

---

## 🪵 2. Standardized Logging for GCP Cloud Logging
* **Problem:** The codebase uses standard `print()` statements (e.g., `print("loading model")`). While Cloud Run captures stdout, standard Python `logging` yields structured logs that integrate seamlessly with Google Cloud Operations (Stackdriver).
* **Improvement Task:**
  - [ ] Replace `print()` statements with standard Python `logging.getLogger("uvicorn")` or configure a custom logger.
  - [ ] Format logs as JSON so Cloud Run can parse severity levels (e.g., INFO, WARNING, ERROR) automatically.

---

## ⚙️ 3. Robust Config Management with Pydantic-Settings
* **Problem:** Environment variables are loaded manually using `dotenv` and `os.environ.get()` in `app/aimodel.py` (with manual type conversions for floats/ints).
* **Improvement Task:**
  - [ ] Use `pydantic-settings` (already included in `requirements.txt`) to create a configuration model. This gives you automatic environment variable mapping, type casting, validation, and default values.
  - *Hint:*
    ```python
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        model_path: str = "models/best.pt"
        save_output: bool = False
        confidence: float = 0.5
        image_size: int = 640

        class Config:
            env_file = ".env"
    ```

---

## 🧪 4. Enhanced Automated Testing
* **Problem:** The test suite is lightweight. It runs YOLOv8 model inference on actual files, which can be slow and resource-intensive in a CI/CD environment.
* **Improvement Tasks:**
  - [ ] **Mocking YOLO Inference:** Write a test that mocks `app.aimodel.model` to return fake bounding boxes, allowing you to test the API's validation/SVG generation path in milliseconds without loading the 50MB model weights.
  - [ ] **Validation Edge Cases:** Add tests for unsupported file types (e.g., submitting a text file to `/predict`) and verify that it returns a clean error.

---

## 🐳 5. Docker Optimizations
* **Problem:** The `Dockerfile` copies the entire directory, including `tests/`, `notebooks/`, and other local files, increasing image size.
* **Improvement Tasks:**
  - [ ] Update `.dockerignore` to explicitly ignore notebooks, tests, raw weights, virtual environments (`venv/`), and any temporary directories.
  - [ ] Build a multi-stage Docker build to keep the production runtime image as lean and fast-loading as possible.
