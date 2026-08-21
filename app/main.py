from fastapi import FastAPI

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