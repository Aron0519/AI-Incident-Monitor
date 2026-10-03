import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_incident(
    service_name: str,
    severity: str,
    message: str
) -> str:
    prompt = f"""
You are an AI incident analysis assistant for a software monitoring platform.

Analyze the following service incident:

Service: {service_name}
Severity: {severity}
Incident message: {message}

Provide:
1. A short explanation of what likely happened.
2. Possible causes.
3. Recommended next steps.

Keep the response concise and practical for a software developer.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text

def classify_incident(
    service_name: str,
    message: str
) -> dict:

    prompt = f"""
You are an incident severity classification assistant.

Analyze this incident:

Service: {service_name}
Incident: {message}

Classify its severity using these levels:

low: Minor issue with minimal impact.
medium: Degraded functionality.
high: Major service disruption.
critical: Complete outage or severe system failure.

Provide:
1. severity: low, medium, high, or critical
2. priority: low, medium, high, or urgent
3. recommended_action: One specific action to investigate
   or resolve the incident.

Return ONLY a valid JSON object with exactly these keys:
"severity", "priority", "recommended_action"

Do not include Markdown or additional explanations.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    result = json.loads(response.output_text)

    return result