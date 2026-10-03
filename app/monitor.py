import asyncio
import httpx

from app.database import get_db
from app.models import Service, Incident, IncidentEvent, Notification



# How often the monitor checks services
CHECK_INTERVAL = 30


async def check_all_services():
    """
    Check every registered service and update its status.
    Create an incident when a service goes down.
    Resolve an incident when a service comes back up.
    """

    # Get a database session
    db_generator = get_db()
    db = next(db_generator)

    try:
        # Get every registered service
        services = db.query(Service).all()

        # Check each service
        for service in services:

            try:
                # Try to contact the service
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(service.url)

                # Service is working
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
                    # Service responded with an error
                    service.status = "down"

                    # Check if an open incident already exists
                    open_incident = db.query(Incident).filter(
                        Incident.service_id == service.id,
                        Incident.status == "open"
                    ).first()

                    # Only create a new incident if one isn't already open
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

                        # Create notification for HTTP errors
                        notification = Notification(
                            incident_id=new_incident.id,
                            message=(
                                f"{severity.upper()} ALERT: "
                                f"{service.name} returned HTTP {response.status_code}"
                            )
                        )

                        db.add(notification)


            except httpx.RequestError:
                # Service could not be reached
                service.status = "down"

                # Check if an open incident already exists
                open_incident = db.query(Incident).filter(
                    Incident.service_id == service.id,
                    Incident.status == "open"
                ).first()

                # Only create a new incident if one isn't already open
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


                    # Create notification for connection failures
                    notification = Notification(
                        incident_id=new_incident.id,
                        message=(
                            f"CRITICAL ALERT: "
                            f"{service.name} could not be reached"
                        )
                    )

                    db.add(notification)

        # Save all changes
        db.commit()

    finally:
        # Close the database session
        db.close()


async def monitor_services():
    """
    Continuously monitor all registered services.
    """

    while True:
        try:
            await check_all_services()

        except Exception as error:
            print(f"Monitoring error: {error}")

        # Wait before checking again
        await asyncio.sleep(CHECK_INTERVAL)