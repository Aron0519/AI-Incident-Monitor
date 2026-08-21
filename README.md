# AI Incident Monitor

A backend API built with FastAPI for monitoring services and managing AI-related incidents.

## Overview

AI Incident Monitor is a backend project designed to provide a foundation for monitoring services, checking system health, and managing incidents through a REST API.

The project is currently in its initial development stage and will be expanded with additional incident monitoring and management features.

## Technologies

- Python
- FastAPI
- Uvicorn
- Git & GitHub

## Current Features

- FastAPI application setup
- Root API endpoint
- Health check endpoint
- Automatic API documentation with Swagger UI
- Development server with automatic reload

## API Endpoints

### GET `/`

Returns the current status of the API.

Example response:

```json
{
  "message": "AI Incident Monitoring Platform API",
  "status": "running"
}
```

### GET `/health`

Checks whether the API is healthy.

Example response:

```json
{
  "status": "healthy"
}
```

## Running the Project

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

Start the development server:

```bash
fastapi dev app/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
AI-Incident-Monitor/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── .gitignore
└── README.md
```

## Future Improvements

- Incident creation and management
- Incident severity classification
- AI-based incident detection
- Service monitoring
- Database integration
- Authentication and authorization
- Logging and alerting
- Dashboard for monitoring incidents
