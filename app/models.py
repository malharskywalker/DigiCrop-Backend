from datetime import date
from pydantic import BaseModel, Field, field_validator


class SensorData(BaseModel):
    PK: str = Field(..., description="Partition key / plot ID", examples=["PLOT#001"])
    SK: str = Field(..., description="Sort key / timeseries key", examples=["TS#2026-06-10"])
    date: date
    temp: float
    humidity: float
    rainfall: float
    wind_speed: float
    N: int
    P: int
    K: int

    @field_validator("PK")
    @classmethod
    def validate_pk(cls, value: str) -> str:
        if not value.startswith("PLOT#"):
            raise ValueError("PK must start with 'PLOT#'")
        return value

    @field_validator("SK")
    @classmethod
    def validate_sk(cls, value: str) -> str:
        if not value.startswith("TS#"):
            raise ValueError("SK must start with 'TS#'")
        return value


class PlotTelemetryResponse(BaseModel):
    plot_id: str
    total_records: int
    latest_reading: SensorData
    timeseries: list[SensorData]


class MessageResponse(BaseModel):
    message: str
    record: SensorData