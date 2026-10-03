# AI Incident Monitoring Platform

An AI-powered service monitoring and incident management platform built with Python, FastAPI, PostgreSQL, OpenAI, and Streamlit.

## Overview

AI Incident Monitor is a full-stack monitoring application designed to track service availability, automatically detect failures, manage incidents, and provide AI-generated troubleshooting recommendations.

The platform continuously monitors registered services and creates incidents when failures occur. It stores incident history in PostgreSQL, generates notifications, and provides a Streamlit dashboard for viewing service health and investigating incidents.

OpenAI integration enables AI-powered incident analysis, severity classification, and recommended troubleshooting actions.

## Features

**Service Monitoring**

* Register and manage services through REST API endpoints.
* Automatically monitor registered services every 30 seconds.
* Track service availability and detect HTTP errors or connection failures.
* Automatically resolve incidents when services recover.

**Incident Management**

* Automatically create incidents when service failures are detected.
* Assign incident severity levels based on detected failures.
* Store incidents and their associated events in PostgreSQL.
* Track incident creation and resolution.
* Prevent duplicate open incidents for the same service.

**AI-Powered Incident Analysis**

* Analyze incidents using OpenAI.
* Generate explanations of potential causes.
* Suggest troubleshooting steps and recommended actions.
* Provide AI-generated severity classifications and priorities.

**Notifications**

* Automatically generate notifications for newly detected incidents.
* Store notification history in PostgreSQL.
* Retrieve notifications through REST API endpoints.
* Mark notifications as read.

**Interactive Dashboard**

* Display total registered services.
* Monitor services that are currently up or down.
* Display active incident counts.
* View registered services and incident history.
* Request AI-powered incident analysis.
* View notifications and mark them as read.

## Technology Stack

| Technology   | Purpose                                 |
| ------------ | --------------------------------------- |
| Python       | Primary programming language            |
| FastAPI      | REST API backend                        |
| PostgreSQL   | Relational database                     |
| SQLAlchemy   | Database ORM                            |
| OpenAI API   | AI incident analysis and classification |
| Streamlit    | Interactive web dashboard               |
| HTTPX        | Asynchronous service monitoring         |
| Requests     | Dashboard-to-backend communication      |
| Pandas       | Data handling                           |
| Uvicorn      | ASGI application server                 |
| Git & GitHub | Version control                         |

## Project Structure

```text
AI-Incident-Monitor/
│
├── app/
│   ├── __init__.py
│   ├── ai_analysis.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── monitor.py
│   └── services.py
│
├── dashboard.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd AI-Incident-Monitor
```

Replace `YOUR_REPOSITORY_URL` with the actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the virtual environment.

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Install and start PostgreSQL.

Create the project database:

```bash
createdb incident_monitor
```

Create a `.env` file in the project's root directory and add:

```dotenv
DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/incident_monitor
OPENAI_API_KEY=your_openai_api_key
```

Replace `YOUR_USERNAME` with your PostgreSQL username and provide your own OpenAI API key.

Initialize the database tables:

```bash
python -m app.init_db
```

This command creates missing database tables without deleting existing data.

Never commit your `.env` file or API keys to GitHub.


### 5. Start the FastAPI backend

```bash
fastapi dev app/main.py
```

The backend runs at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### 6. Start the Streamlit dashboard

Open a second terminal, activate your virtual environment, and run:

```bash
streamlit run dashboard.py
```

The dashboard will normally be available at:

http://localhost:8501

Keep both FastAPI and Streamlit running while using the application.

## API Endpoints

### General

| Method | Endpoint  | Description      |
| ------ | --------- | ---------------- |
| GET    | `/`       | API information  |
| GET    | `/health` | API health check |

### Service Management

| Method | Endpoint                              | Description                  |
| ------ | ------------------------------------- | ---------------------------- |
| POST   | `/api/v1/services`                    | Register a service           |
| GET    | `/api/v1/services`                    | Retrieve registered services |
| POST   | `/api/v1/services/{service_id}/check` | Manually check a service     |

### Incident Management

| Method | Endpoint                                 | Description              |
| ------ | ---------------------------------------- | ------------------------ |
| GET    | `/api/v1/incidents`                      | Retrieve incidents       |
| GET    | `/api/v1/incidents/{incident_id}`        | Retrieve an incident     |
| DELETE | `/api/v1/incidents/{incident_id}`        | Delete an incident       |
| GET    | `/api/v1/incidents/{incident_id}/events` | Retrieve incident events |

### AI Analysis

| Method | Endpoint                                   | Description                                             |
| ------ | ------------------------------------------ | ------------------------------------------------------- |
| GET    | `/api/v1/incidents/{incident_id}/analysis` | Generate AI incident analysis                           |
| GET    | `/api/v1/incidents/{incident_id}/classify` | Generate AI severity classification and recommendations |

### Notifications

| Method | Endpoint                                       | Description                 |
| ------ | ---------------------------------------------- | --------------------------- |
| GET    | `/api/v1/notifications`                        | Retrieve notifications      |
| PATCH  | `/api/v1/notifications/{notification_id}/read` | Mark a notification as read |

For interactive endpoint documentation, visit `/docs` while the backend is running.

## How It Works

1. Users register services through the FastAPI REST API.
2. The monitoring system checks registered services every 30 seconds.
3. When a service fails, the application creates an incident and records an event.
4. The notification system generates an alert for the newly detected incident.
5. Incident information and notifications are stored in PostgreSQL.
6. Users access the Streamlit dashboard to view service health and incident history.
7. Users can request AI-generated analysis and troubleshooting recommendations.
8. When a service recovers, the monitoring system automatically resolves its open incidents.

## Dashboard

The Streamlit dashboard provides a centralized interface for monitoring registered services and investigating incidents.

Its main components include:

* Live service monitoring statistics
* Registered service information
* Incident history
* AI-powered incident analysis
* Interactive incident notifications

## Security Notes

* API keys are stored in environment variables.
* The `.env` file is excluded from version control.
* AI-generated troubleshooting recommendations should be verified before applying them to production systems.

## Future Improvements

* User authentication and authorization
* Email or Slack notifications
* Historical monitoring charts
* Automated testing
* Database migrations
* Containerization with Docker
* Cloud deployment

## Project Status

The core monitoring platform, AI integration, PostgreSQL persistence, notification system, and Streamlit dashboard have been implemented and tested locally.
