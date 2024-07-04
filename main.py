import uvicorn
from fastapi import FastAPI
from app.routes import router as app_router
from app.metrics import init_metrics  # Import the init_metrics function

app = FastAPI()

# Initialize metrics
init_metrics(app)

# Include your application routes
app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
