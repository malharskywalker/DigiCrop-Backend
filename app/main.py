from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.models import SensorData, PlotTelemetryResponse, MessageResponse
from app.services import get_plot_sensor_data, add_sensor_data

app = FastAPI(
    title="DigiCrop Crop Sensor API",
    description="Backend API for crop telemetry ingestion and retrieval using a JSON file as a mock NoSQL database.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "DigiCrop Sensor API is running",
        "docs": "/docs"
    }


@app.get(
    "/api/v1/crop-sensor-data/{plot_id}",
    response_model=PlotTelemetryResponse,
    summary="Retrieve telemetry data for a plot"
)
def fetch_crop_sensor_data(plot_id: str):
    return get_plot_sensor_data(plot_id)


@app.post(
    "/api/v1/crop-sensor-data",
    response_model=MessageResponse,
    status_code=201,
    summary="Ingest a new telemetry record"
)
def create_crop_sensor_data(payload: SensorData):
    return add_sensor_data(payload)