import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text):
    prompt = f"""
You are an AI assistant that generates clean, structured, highly accurate meeting summaries.

Your task:
Summarize the following meeting transcript into clear bullet points covering:
- Key discussion points
- Decisions taken
- Problems or blockers
- Important clarifications
- Any conclusions

Make it concise, readable, and professional.

Transcript:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400
    )

    return response.choices[0].message["content"].strip()


def extract_action_items(text):
    prompt = f"""
Extract ALL action items from the following meeting transcript.

Return ONLY a JSON list. 
Each item MUST follow this format:
{{
  "assignee": "Name of the person responsible",
  "deadline": "Specific deadline or 'Not specified'",
  "task": "What exactly needs to be done"
}}

Transcript:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=300
    )

    import json
    try:
        return json.loads(response.choices[0].message["content"])
    except:
        # fallback
        return []


def run_pipeline(text):
    summary = generate_summary(text)
    actions = extract_action_items(text)
    return summary, actions

