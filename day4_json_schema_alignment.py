import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


candidate_profile_context = """
Candidate Name: Rahul Kumar
Email: rahul.kumar@example.com
Phone: +91 9123456789
Location: Hyderabad, Telangana
Experience: 2 years
Current Role: GenAI Engineer
Education: B.Tech in Computer Science
Primary Skills: Python, Java, Prompt Engineering, REST APIs, Git, SQL
Domain: Generative AI
Availability: Immediate
"""


json_alignment_instruction = """
Act as a candidate profile transformation service.

Convert the supplied candidate information into one valid JSON object.

The JSON must contain:
@context
@type
name
email
telephone
address
jobTitle
experience
education
skills
domain
availability

Rules:
- Return JSON only.
- Do not use Markdown code fences.
- Do not add explanations before or after the JSON.
- Keep the response on a single line.
- Use only information provided in the candidate profile.
- Do not invent missing candidate information.
"""


def build_candidate_schema(profile):

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            max_tokens=500,
            messages=[
                {
                    "role": "system",
                    "content": json_alignment_instruction
                },
                {
                    "role": "user",
                    "content": profile
                }
            ]
        )

        result_text = response.choices[0].message.content.strip()

        try:
            validated_data = json.loads(result_text)
            return validated_data

        except json.JSONDecodeError:
            return {
                "status": "error",
                "message": "The model returned invalid JSON."
            }

    except Exception as error:
        return {
            "status": "error",
            "message": f"API execution failed: {error}"
        }


print("----- Candidate Schema Processing -----")

candidate_data = build_candidate_schema(candidate_profile_context)

print(json.dumps(candidate_data, separators=(",", ":")))