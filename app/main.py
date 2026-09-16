from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
import asyncio
from sqlalchemy.orm import Session
import httpx
from app.services import ServiceCreate, ServiceResponse, IncidentResponse, IncidentEventResponse
from app.database import get_db
from app.models import Service, Incident, IncidentEvent
from app.monitor import monitor_services

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start automatic service monitoring
    monitoring_task = asyncio.create_task(monitor_services())

    print("Automatic service monitoring started.")

    yield

    # Stop monitoring when the application shuts down
    monitoring_task.cancel()

    try:
        await monitoring_task
    except asyncio.CancelledError:
        pass

    print("Automatic service monitoring stopped.")

# app creates our central object representing our backend server
# app basically creates our FastAPI application
app = FastAPI(
    title="AI Incident Monitoring Platform",
    description="Backend API for monitoring services and managing incidents.",
    version="0.1.0",
    lifespan=lifespan 
)

# When someone sends an HTTP GET request to /, execute the function below.
@app.get("/")
def root():
    return {
        "message": "AI Incident Monitoring Platform API",
        "status": "running"
    }

# this is another endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# when someone sends an HTTP POST request to /api/v1/services, execute the function below.
#the response from this endpoint must follow the ServiceResponse structure defined in services.py.
# FastAPI expects the request body to follow the structure defined in the service.py 
@app.post("/api/v1/services", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(
        name=service.name,
        url=str(service.url)
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service

@app.get("/api/v1/services", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@app.put("/api/v1/services/{service_id}/url")
def update_service_url(
    service_id: int,
    url: str,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.url = url

    db.commit()
    db.refresh(service)

    return service

# Add the health check endpoint
@app.post("/api/v1/services/{service_id}/check")
async def check_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    # Find the service in the database
    service = db.query(Service).filter(Service.id == service_id).first()

    # If the service does not exist, return 404
    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    try:
        # Try to contact the service
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(service.url)

        # If the service responds successfully
        if response.status_code < 400:
            service.status = "up"

            # Resolve any existing open incidents
            open_incidents = db.query(Incident).filter(
                Incident.service_id == service.id,
                Incident.status == "open"
            ).all()

            for incident in open_incidents:
                incident.status = "resolved"

                # Record that the incident was resolved
                resolved_event = IncidentEvent(
                    incident_id=incident.id,
                    event_type="resolved",
                    message="Service has recovered"
                )

                db.add(resolved_event)

        else:
            # Service responded, but with an error
            service.status = "down"

            # Check if an open incident already exists
            open_incident = db.query(Incident).filter(
                Incident.service_id == service.id,
                Incident.status == "open"
            ).first()

            # Only create a new incident if one is not already open
            if not open_incident:

                if response.status_code >= 500:
                    severity = "high"
                else:
                    severity = "medium"

                new_incident = Incident(
                    service_id=service.id,
                    status="open",
                    severity=severity,
                    message=f"Service returned HTTP {response.status_code}"
                )

                db.add(new_incident)

                # Get the new incident's ID
                db.flush()

                # Record that the incident was created
                created_event = IncidentEvent(
                    incident_id=new_incident.id,
                    event_type="created",
                    message=f"Incident created: Service returned HTTP {response.status_code}"
                )

                db.add(created_event)

    except httpx.RequestError:
        # Service could not be reached
        service.status = "down"

        # Check if an open incident already exists
        open_incident = db.query(Incident).filter(
            Incident.service_id == service.id,
            Incident.status == "open"
        ).first()

        # Only create a new incident if one is not already open
        if not open_incident:
            new_incident = Incident(
                service_id=service.id,
                status="open",
                severity="critical",
                message="Service could not be reached"
            )

            db.add(new_incident)

            # Get the new incident's ID
            db.flush()

            # Record that the incident was created
            created_event = IncidentEvent(
                incident_id=new_incident.id,
                event_type="created",
                message="Incident created: Service could not be reached"
            )

            db.add(created_event)

    # Save changes to PostgreSQL
    db.commit()
    db.refresh(service)

    return {
        "service_id": service.id,
        "service_name": service.name,
        "status": service.status
    }

@app.get("/api/v1/incidents", response_model=list[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

@app.get("/api/v1/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@app.delete("/api/v1/incidents/{incident_id}")
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)
    db.commit()

    return {"message": "Incident deleted successfully"}


@app.get(
    "/api/v1/incidents/{incident_id}/events",
    response_model=list[IncidentEventResponse]
)
def get_incident_events(
    incident_id: int,
    db: Session = Depends(get_db)
):
    # Make sure the incident exists
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    # Get all events for this incident
    events = db.query(IncidentEvent).filter(
        IncidentEvent.incident_id == incident_id
    ).order_by(IncidentEvent.created_at).all()

    return events