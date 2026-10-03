import os

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