from datetime import datetime
from fastapi import HTTPException, status

from app.models import SensorData
from app.utils import read_data, write_data


def get_plot_sensor_data(plot_id: str) -> dict:
    """
    Fetch all telemetry records for a given plot ID,
    sort them chronologically, and return latest reading.
    """
    data = read_data()
    records = data.get("timeseries", [])

    filtered_records = [record for record in records if record.get("PK") == plot_id]

    if not filtered_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No records found for plot_id '{plot_id}'"
        )

    filtered_records.sort(
        key=lambda record: datetime.strptime(record["date"], "%Y-%m-%d")
    )

    latest_record = filtered_records[-1]

    return {
        "plot_id": plot_id,
        "total_records": len(filtered_records),
        "latest_reading": latest_record,
        "timeseries": filtered_records
    }


def add_sensor_data(payload: SensorData) -> dict:
    """
    Validate and append a new telemetry record to the JSON database.
    Prevent duplicate PK + SK combinations.
    """
    data = read_data()

    if "timeseries" not in data or not isinstance(data["timeseries"], list):
        data["timeseries"] = []

    # Convert Pydantic model to dict
    new_record = payload.model_dump()

    # Convert date object to string for JSON storage
    new_record["date"] = payload.date.isoformat()

    # Optional integrity check:
    # ensure SK date matches the date field
    expected_sk = f"TS#{payload.date.isoformat()}"
    if payload.SK != expected_sk:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"SK must match the date field. Expected '{expected_sk}' for date '{payload.date.isoformat()}'."
        )

    # Prevent duplicates based on PK + SK
    for record in data["timeseries"]:
        if record.get("PK") == new_record["PK"] and record.get("SK") == new_record["SK"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A record with the same PK and SK already exists."
            )

    data["timeseries"].append(new_record)
    write_data(data)

    return {
        "message": "Sensor data added successfully",
        "record": new_record
    }