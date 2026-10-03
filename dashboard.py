import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

# Configure the dashboard
st.set_page_config(
    page_title="AI Incident Monitor",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI Incident Monitoring Dashboard")
st.write("Monitor your services, incidents, and notifications.")

st.divider()

# Check whether the backend is running
try:
    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )
    response.raise_for_status()

    st.success("Backend connected successfully!")

except requests.RequestException:
    st.error(
        "Cannot connect to FastAPI. "
        "Make sure your backend is running."
    )

st.subheader("Live Monitoring Overview")

try:
    services_response = requests.get(
        f"{API_URL}/api/v1/services",
        timeout=5
    )

    incidents_response = requests.get(
        f"{API_URL}/api/v1/incidents",
        timeout=5
    )

    services_response.raise_for_status()
    incidents_response.raise_for_status()

    services = services_response.json()
    incidents = incidents_response.json()

    # Calculate dashboard statistics
    total_services = len(services)

    services_up = sum(
        1 for service in services
        if service["status"] == "up"
    )

    services_down = sum(
        1 for service in services
        if service["status"] == "down"
    )

    active_incidents = sum(
        1 for incident in incidents
        if incident["status"] == "open"
    )

    # Create four dashboard columns
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Services", total_services)
    col2.metric("Services Up", services_up)
    col3.metric("Services Down", services_down)
    col4.metric("Active Incidents", active_incidents)

except requests.RequestException as error:
    st.error(f"Unable to load monitoring statistics: {error}")


# Display service information
st.divider()
st.subheader("Registered Services")

if "services" in locals():
    if services:
        st.dataframe(
            services,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No registered services found.")


# Display incident information
st.divider()
st.subheader("Incident History")

if "incidents" in locals():
    if incidents:
        st.dataframe(
            incidents,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No incidents found.")

# AI-powered incident analysis
st.divider()
st.subheader("AI Incident Analysis")

if "incidents" in locals() and incidents:

    # Create a dropdown containing available incidents
    incident_options = {
        f"Incident {incident['id']} - {incident['service_name']}": incident["id"]
        for incident in incidents
    }

    selected_incident = st.selectbox(
        "Select an incident to analyze",
        options=list(incident_options.keys())
    )

    # Only call OpenAI when the user clicks the button
    if st.button("Analyze Incident with AI"):

        incident_id = incident_options[selected_incident]

        try:
            with st.spinner("AI is analyzing the incident..."):

                response = requests.get(
                    f"{API_URL}/api/v1/incidents/{incident_id}/analysis",
                    timeout=90
                )

                response.raise_for_status()
                analysis = response.json()

            st.success("Analysis completed!")

            # Display the incident ID
            st.subheader(f"AI Analysis for Incident {incident_id}")

            # Extract the analysis text from the API response
            analysis_text = analysis.get(
                "analysis",
                "No analysis available."
            )

            # Convert escaped newline characters into actual line breaks
            analysis_text = analysis_text.replace("\\n", "\n")

            # Display the analysis in a readable format
            st.markdown(analysis_text)

        except requests.RequestException as error:
            st.error(f"AI analysis failed: {error}")

else:
    st.info("No incidents available for AI analysis.")

# Display incident notifications
st.divider()
st.subheader("Incident Notifications")

try:
    response = requests.get(
        f"{API_URL}/api/v1/notifications",
        timeout=5
    )
    response.raise_for_status()

    notifications = response.json()

    if notifications:
        for notification in notifications:

            # Display notification information
            with st.container(border=True):

                if notification["is_read"]:
                    st.write("✅ Read")
                else:
                    st.warning("🔔 Unread Notification")

                st.write(notification["message"])

                st.caption(
                    f"Incident ID: {notification['incident_id']}"
                )

                # Allow users to mark unread notifications as read
                if not notification["is_read"]:

                    if st.button(
                        "Mark as Read",
                        key=f"notification_{notification['id']}"
                    ):

                        update_response = requests.patch(
                            f"{API_URL}/api/v1/notifications/"
                            f"{notification['id']}/read",
                            timeout=5
                        )

                        update_response.raise_for_status()

                        st.rerun()

    else:
        st.info("No notifications available.")

except requests.RequestException as error:
    st.error(f"Unable to load notifications: {error}")