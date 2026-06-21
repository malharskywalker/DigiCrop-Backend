# DigiCrop Backend 

A FastAPI-based backend service for managing **crop sensor telemetry data** using a JSON file as a mock NoSQL datastore.

This project was built as part of a backend/API development assignment and demonstrates:

* **REST API design with FastAPI**
* **Pydantic-based request validation**
* **JSON file persistence**
* **Retrieval of plot-level timeseries sensor data**
* **Insertion of new sensor readings**
* **API testing via Postman**

---

# Table of Contents

* [Project Overview](#project-overview)
* [Assignment Objective](#assignment-objective)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Dataset Format](#dataset-format)
* [API Endpoints](#api-endpoints)

  * [GET Plot Sensor Data](#1-get-apiv1crop-sensor-dataplot_id)
  * [POST New Sensor Reading](#2-post-apiv1crop-sensor-data)
* [Validation Rules](#validation-rules)
* [Error Handling](#error-handling)
* [How the Application Works](#how-the-application-works)
* [Setup Instructions](#setup-instructions)
* [Run the Application](#run-the-application)
* [API Testing with Postman](#api-testing-with-postman)
* [Screenshots](#screenshots)
* [Design Decisions](#design-decisions)
* [Dataset Note](#dataset-note)
* [Future Improvements](#future-improvements)

---

# Project Overview

DigiCrop sensors collect daily agricultural telemetry for each plot.
This project exposes a backend API that allows clients to:

1. **Fetch all telemetry records for a specific plot**
2. **Return the latest reading separately**
3. **Add a new daily telemetry record**
4. **Persist updates to a local JSON file safely**

The API is implemented using **FastAPI**, while the data is stored in a JSON file to simulate a lightweight NoSQL-style datastore.

---

# Assignment Objective

The goal of this assignment is to build a backend service that can:

* Read plot-level telemetry data from a JSON file
* Serve that data through a clean API
* Accept new telemetry records through POST requests
* Validate payloads before saving them
* Handle missing plots, duplicate entries, and invalid payloads gracefully
* Demonstrate the API using **Postman screenshots or an exported Postman collection**

---

# Features

## Implemented Features

* **GET plot telemetry** by plot ID
* **POST new sensor telemetry** into the dataset
* Return the **latest reading** separately for easier dashboard consumption
* Sort and return the full **timeseries history**
* Validate incoming payloads with **Pydantic**
* Prevent invalid or inconsistent records
* Persist data back into the JSON file
* Test the API through **Postman**

---

# Tech Stack

* **Python 3**
* **FastAPI**
* **Pydantic**
* **Uvicorn**
* **JSON file storage**
* **Postman** for API testing

---

# Project Structure

```bash
digicrop-assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   └── utils.py
│
├── data/
│   └── plot_sensor_data.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Dataset Format

The telemetry data is stored in:

```bash
data/plot_sensor_data.json
```

The file contains a top-level `timeseries` array, where each item represents a daily reading for a plot.

## Example record

```json
{
  "PK": "PLOT#001",
  "SK": "TS#2026-06-10",
  "date": "2026-06-10",
  "temp": 34.1,
  "humidity": 59,
  "rainfall": 1.2,
  "wind_speed": 11.0,
  "N": 38,
  "P": 28,
  "K": 55
}
```

---

# API Endpoints

# 1) GET `/api/v1/crop-sensor-data/{plot_id}`

Fetch all telemetry records for a plot and return the latest reading separately.

## Example request

```http
GET /api/v1/crop-sensor-data/PLOT%23001
```

> `#` must be URL-encoded in the browser/Postman URL.
> Example: `PLOT#001` becomes `PLOT%23001`

---

## Example success response (`200 OK`)

```json
{
  "plot_id": "PLOT#001",
  "total_records": 10,
  "latest_reading": {
    "PK": "PLOT#001",
    "SK": "TS#2026-06-10",
    "date": "2026-06-10",
    "temp": 34.1,
    "humidity": 59,
    "rainfall": 1.2,
    "wind_speed": 11.0,
    "N": 38,
    "P": 28,
    "K": 55
  },
  "timeseries": [
    {
      "PK": "PLOT#001",
      "SK": "TS#2026-06-01",
      "date": "2026-06-01",
      "temp": 32.5,
      "humidity": 65,
      "rainfall": 12.0,
      "wind_speed": 14.2,
      "N": 45,
      "P": 30,
      "K": 60
    }
  ]
}
```

---

## Example not found response (`404 Not Found`)

```json
{
  "detail": "No records found for plot_id 'PLOT#999'"
}
```

---

# 2) POST `/api/v1/crop-sensor-data`

Add a new sensor telemetry reading to the dataset.

## Example request body

```json
{
  "PK": "PLOT#001",
  "SK": "TS#2026-06-11",
  "date": "2026-06-11",
  "temp": 33.0,
  "humidity": 62,
  "rainfall": 2.5,
  "wind_speed": 10.7,
  "N": 37,
  "P": 27,
  "K": 54
}
```

---

## Example success response (`201 Created`)

```json
{
  "message": "Sensor data added successfully",
  "record": {
    "PK": "PLOT#001",
    "SK": "TS#2026-06-11",
    "date": "2026-06-11",
    "temp": 33.0,
    "humidity": 62.0,
    "rainfall": 2.5,
    "wind_speed": 10.7,
    "N": 37,
    "P": 27,
    "K": 54
  }
}
```

---

# Validation Rules

The project validates incoming telemetry records before saving them.

## Validation checks

* `PK` must represent a valid plot key (for example: `PLOT#001`)
* `SK` should follow the format:

  ```text
  TS#YYYY-MM-DD
  ```
* `date` must be a valid date
* Numeric fields must be valid numbers
* Required fields must be present
* `SK` and `date` must match logically

  * Example:

    * `date = 2026-06-11`
    * `SK = TS#2026-06-11`

---

# Error Handling

The API returns meaningful HTTP responses for common failure scenarios.

## Common error cases

| Scenario                 | Status Code   | Example                             |
| ------------------------ | ------------- | ----------------------------------- |
| Plot not found           | `404`         | GET unknown plot                    |
| Duplicate record         | `400`         | Same `PK + SK` already exists       |
| Invalid payload          | `422` / `400` | Wrong field format / missing values |
| `SK` and `date` mismatch | `400`         | `SK` date does not match `date`     |

---

## Example duplicate record error

```json
{
  "detail": "A record with the same PK and SK already exists."
}
```

---

## Example validation error

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "PK"],
      "msg": "Invalid plot key format"
    }
  ]
}
```

---

# How the Application Works

The project is divided into logical backend layers:

## `app/models.py`

Contains the **Pydantic data model** used to validate incoming sensor data.

---

## `app/utils.py`

Contains helper functions such as:

* reading the JSON file
* writing updated data back to the file
* reusable utility logic

---

## `app/services.py`

Contains the main business logic for:

* retrieving plot telemetry
* filtering plot records
* sorting records
* identifying the latest reading
* adding a new record
* checking duplicates

---

## `app/main.py`

Defines the FastAPI application and exposes the API routes.

---

# Setup Instructions

## 1) Clone the repository

```bash
git clone https://github.com/malharskywalker/DigiCrop-Backend.git
cd DigiCrop-Backend
```

---

## 2) Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

If the server starts successfully, it will run at:

```text
http://127.0.0.1:8000
```

---

## Swagger API documentation

FastAPI automatically provides Swagger UI here:

```text
http://127.0.0.1:8000/docs
```

You can test the endpoints directly from the browser using Swagger as well.

---

# API Testing with Postman

The assignment also requires **API testing using Postman**.
This repository can include either:

* an **exported Postman collection**, or
* **clear screenshots** of the tested requests and responses

---

## Recommended Postman test cases

### 1. GET existing plot

Request:

```http
GET http://127.0.0.1:8000/api/v1/crop-sensor-data/PLOT%23001
```

Expected:

* `200 OK`
* `plot_id = PLOT#001`
* `total_records = 10`
* `latest_reading` contains the most recent record

---

### 2. POST valid sensor record

Request:

```http
POST http://127.0.0.1:8000/api/v1/crop-sensor-data
```

Body:

```json
{
  "PK": "PLOT#001",
  "SK": "TS#2026-06-11",
  "date": "2026-06-11",
  "temp": 33.0,
  "humidity": 62,
  "rainfall": 2.5,
  "wind_speed": 10.7,
  "N": 37,
  "P": 27,
  "K": 54
}
```

Expected:

* `201 Created`
* response contains inserted record

---

### 3. POST duplicate record

Send the same payload again.

Expected:

* `400 Bad Request`
* duplicate error message

---

### 4. GET non-existing plot

Request:

```http
GET http://127.0.0.1:8000/api/v1/crop-sensor-data/PLOT%23999
```

Expected:

* `404 Not Found`

---

# Screenshots

---

### Swagger Docs
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/708920ba-69d9-48e8-9fc4-3b98a25be761" />


### GET Request Success in Postman
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/81f36d87-d6c2-45bf-8e80-cfaeb8d8da77" />

### POST Request Success in Postman
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/fbae011d-c7d7-498d-818f-256b82632c71" />

### Duplicate Record Error
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/69c69d5b-43b5-4612-8cd2-06c9c44e8f67" />


### Plot Not Found Error
<img width="960" height="600" alt="image" src="https://github.com/user-attachments/assets/107a0062-a67b-4f4e-82bc-23892b744f0d" />

---

# Design Decisions

## Why FastAPI?

FastAPI was chosen because it provides:

* fast API development
* automatic request validation with Pydantic
* built-in Swagger/OpenAPI docs
* clean route declaration and JSON handling

---

## Why JSON file storage?

The assignment required a file-based data source.
Using a JSON file is a simple way to simulate a NoSQL datastore while still demonstrating:

* read operations
* append operations
* validation
* update persistence
* error handling

---

## Why separate `models`, `services`, and `utils`?

This separation makes the project more maintainable:

* **models.py** → data validation layer
* **services.py** → business logic layer
* **utils.py** → file and helper utilities
* **main.py** → API routing layer

This structure is cleaner than putting everything in one file and is closer to a real backend project layout.

---

# Conclusion

This project demonstrates a complete backend workflow for managing agricultural telemetry data:

* storing sensor readings in a JSON-based mock datastore
* retrieving plot telemetry through a REST API
* ingesting new daily sensor data
* validating payloads
* handling errors cleanly
* and testing the API through Postman

It is designed to be simple, readable, and aligned with the DigiCrop backend assignment requirements.
