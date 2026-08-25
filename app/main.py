from fastapi import FastAPI, HTTPException
import httpx
from app.services import ServiceCreate, ServiceResponse, IncidentResponse

#temporary in-memory storage for services
services = []

# temporary in-memory storage for incidents
incidents = []

# app creates our central object representing our backend server
# app basically creates our FastAPI application
app = FastAPI(
    title="AI Incident Monitoring Platform",
    description="Backend API for monitoring services and managing incidents.",
    version="0.1.0"
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
def create_service(service: ServiceCreate):
    new_service = {
        "id": len(services) + 1,
        "name": service.name,
        "url": service.url,
        "description": service.description,
        "status": "unknown"
    }

    services.append(new_service)

    return new_service

@app.get("/api/v1/services", response_model=list[ServiceResponse])
def get_services():
    return services


@app.put("/api/v1/services/{service_id}/url")
def update_service_url(service_id: int, url: str):
    for service in services:
        if service["id"] == service_id:
            service["url"] = url
            return service

    raise HTTPException(status_code=404, detail="Service not found")

#add the health check endpoint 
@app.post("/api/v1/services/{service_id}/check")
async def check_service(service_id: int):
    for service in services:
        if service["id"] == service_id:

            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(str(service["url"]))

                if response.status_code < 400:
                    service["status"] = "up"

                    for incident in incidents:
                        if incident["service_id"] == service["id"] and incident["status"] == "open":
                            incident["status"] = "resolved"

                else:
                    service["status"] = "down"

                    open_incident_exists = any(
                        incident["service_id"] == service["id"]
                        and incident["status"] == "open"
                        for incident in incidents
                    )

                    if not open_incident_exists:
                        incidents.append({
                            "id": len(incidents) + 1,
                            "service_id": service["id"],
                            "service_name": service["name"],
                            "status": "open",
                            "message": f"Service returned HTTP {response.status_code}"
                        })

            except httpx.RequestError:
                 service["status"] = "down"

                 open_incident_exists = any(
                    incident["service_id"] == service["id"]
                    and incident["status"] == "open"
                    for incident in incidents
                )

                 if not open_incident_exists:
                    incidents.append({
                        "id": len(incidents) + 1,
                        "service_id": service["id"],
                        "service_name": service["name"],
                        "status": "open",
                        "message": "Service could not be reached"
                    })

            return service

    raise HTTPException(status_code=404, detail="Service not found")

@app.get("/api/v1/incidents", response_model=list[IncidentResponse])
def get_incidents():
    return incidents