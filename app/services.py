from pydantic import BaseModel, HttpUrl


# The data required when someone wants to create a new service
class ServiceCreate(BaseModel):
    name: str
    url: HttpUrl
    description: str | None = None


# The data returned when we work with a service
class ServiceResponse(BaseModel):
    id: int
    name: str
    url: HttpUrl
    description: str | None = None
    status: str


# Represents an incident when a service has a problem
class IncidentResponse(BaseModel):
    id: int
    service_id: int
    service_name: str
    status: str
    message: str