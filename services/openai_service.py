import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_review(tags, language):
    service_name = os.getenv('SERVICE')
    try:
        prompt = (
            f"Write a customer review of over 350 characters about the service ({service_name}). "
            f"Make sure to use all of the following tags in the review: {', '.join(tags)}, and only these tags. "
            f"Do not add any other tags or create new ones. "
            f"Do not mention how long the service was used or any specific time periods. "
            f"Sometimes mention the name of the service ({service_name}), and sometimes do not. "
            f"Start the review in a unique and engaging way each time, avoiding repetitive phrases like 'I recently tried'. "
            f"Keep it simple and relatable. "
            f"Write the review in {language}."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are writing universal customer reviews"},
                {"role": "user", "content": prompt},
            ],
            frequency_penalty=0.6,
            presence_penalty=0.6,
            # temperature=0.7,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "review_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "review": {
                                "description": "One review from the product",
                                "type": "string",
                            },
                        }
                    },
                }
            }
        )
        content = response.choices[0].message.content
        json_content = json.loads(content)
        return json_content.get("review", "No review found.")
    except Exception as e:
        raise RuntimeError(f"OpenAI request failed: {e}")