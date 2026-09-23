
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from schemas.ai_schema import AIAnalysisResponse

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_analysis(
    company_name,
    industry,
    employees,
    security_concerns
):
    prompt = f"""
    Analyze the following company security information.

    Company: {company_name}
    Industry: {industry}
    Employees: {employees}
    Security Concerns: {security_concerns}

    Return ONLY valid JSON in exactly this structure:

    {{
        "risk_summary": "Short risk summary",
        "recommendations": [
            {{
                "recommendation": "Recommendation 1",
                "priority": "Critical"
            }},
            {{
                "recommendation": "Recommendation 2",
                "priority": "High"
            }},
            {{
                "recommendation": "Recommendation 3",
                "priority": "Medium"
            }}
        ]
    }}

    Do not use Markdown.
    Do not add explanations outside the JSON.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        response_text = response.text.strip()

        # Remove Markdown code fences if Gemini adds them
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")
            response_text = response_text.strip()

        parsed_response = json.loads(response_text)

        validated_response = AIAnalysisResponse.model_validate(
            parsed_response
        )

        return {
            "prompt": prompt,
            "response": validated_response
        }

    except json.JSONDecodeError as e:
        print(f"Invalid JSON returned by Gemini: {e}")

        return {
            "prompt": prompt,
            "response": None
        }

    except errors.ServerError as e:
        print(f"Gemini server error: {e}")
        print("Gemini may be temporarily overloaded. Please try again.")

    return {
        "prompt": prompt,
        "response": None
    }
