# NyayaMitra Deployment Guide

This backend is designed to be highly portable. Since it relies on local NLP models (`spaCy`, `PaddleOCR`), memory constraints on free tiers are the primary consideration. We recommend at least 1GB of RAM for the deployment.

## 1. Local Deployment (Docker)
The easiest way to guarantee the C++ build dependencies (OpenCV) work flawlessly.
```bash
docker-compose up --build -d
```
Your API will be live at `http://localhost:8000`.

## 2. Deploying to Render
1. Create a new "Web Service" on [Render.com](https://render.com).
2. Connect your GitHub repository.
3. Select **Docker** as the runtime environment.
4. Render will automatically detect the `Dockerfile` and build the container.
5. *Note: Choose at least the "Starter" tier ($7/mo) to ensure `PaddleOCR` has enough memory to run.*

## 3. Deploying to Railway
1. Create a New Project on [Railway.app](https://railway.app).
2. Deploy from your GitHub repo.
3. Railway automatically detects the `Dockerfile`.
4. Go to Settings -> Deploy -> and set the Start Command if needed (usually automatic).
5. Expose the port by generating a domain in the Networking tab.

## 4. HuggingFace Spaces
Perfect for free AI hackathon hosting.
1. Create a new Space and select **Docker**.
2. Push this backend code to the Space.
3. HuggingFace will build the image and provide a public URL. This gives you 16GB RAM for free, which is perfect for `PaddleOCR`.
