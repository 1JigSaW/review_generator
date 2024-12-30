import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
service_name = os.getenv('SERVICE')

with open('description.txt', 'r') as file:
    service_description = file.read().strip()


def generate_tags():
    try:
        prompt = (
            f"Analyze the following service: {service_description}. "
            f"Generate a list of 20 simple, clear, and relevant tags that reflect the key features, benefits, and emotions users associate with this service. "
            f"These tags should be short (1-3 words), easy to understand, and helpful for everyday users when writing reviews. "
            f"The tags should be simple enough for users to easily comprehend and use when writing their review, avoiding complex or technical phrases. "
            f"Focus on the practical aspects of the service, its emotional impact on users, and how it improves their experience. "
            f"Avoid generic tags like 'good', 'useful', or 'nice', as well as overly abstract or complex terms that might be difficult to understand. "
            f"The tags should be specific and actionable, making them easy to use in a review of the service."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a tag generation assistant specializing in analyzing products and services."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "tags_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "tags": {
                                "type": "array",
                                "description": "List of tags",
                                "items": {
                                    "type": "string",
                                    "description": "A single tag"
                                }
                            }
                        },
                    },
                }
            }
        )

        content = response.choices[0].message.content
        generated_tags = json.loads(content)
        print(generated_tags)
        return generated_tags.get("tags", [])
    except Exception as e:
        raise RuntimeError(f"OpenAI request for tags failed: {e}")


def generate_review(tags, language):
    try:
        prompt = (
            f"Write a customer review of over 350 characters about the service ({service_name}). "
            f"Make sure to use all of the following tags in the review: {', '.join(tags)}, and only these tags. "
            f"Do not add any other tags or create new ones. "
            f"Do not mention how long the service was used or any specific time periods. "
            f"Sometimes mention the name of the service ({service_name}), and sometimes do not. "
            f"Start the review in a unique and engaging way each time, avoiding repetitive phrases like 'I recently tried'. "
            f"Keep it simple and relatable. "
            # f"Write the review in {language}."
            f"Write content like human talk, who used {service_name}, like user, do not use over passive voice, "
            f"do not use jargons, do not words like - overall, furthermore, in conclusions, that excessively. "
            f"Write a review as if it were written by me, using my personal theses, style, tone and communication that you know about me."
            f"Aim for a Flesch reading score of 80 or higher. Use the active voice and avoid adverbs. Avoid buzzwords and instead use plain English. Avoid being salesy or overly enthusiastic and instead express calm confidence"

        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": "You are a person who writes reviews about web services"},
                {"role": "user", "content": prompt},
            ],
            frequency_penalty=0.6,
            presence_penalty=0.6,
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


def humanize_text(input_text, language):
    try:
        prompt = (
            f"Example 1: Revolut has really literally revolutionised how we transact with each other financially no matter what part of the world one is in. Highly recommend this brilliant app for making banking so easy no matter where in the world I am in. 10/10 👍👍"
            f"Example 2: Love the perks and high rates but miss some features\nI use Revolut for a few months. I moved my finances from bunq. I like their app environment and in general I enjoyed the higher interest rates in Savings. I liked the idea of the Revolut Pro account (focused on freelancers) within the same app and also the <18 for kids. My favorite are the perks. It’s them and the interest rates that keep me staying with Revolut. I’m able to use for free VPN, Perplexity to only mention a few.\nHowever I wished the Revolut Pro has some more freedom. I’m not able to use it for Ideal payments. I also wished Revolut would make it possible to open more than one account with the same currency. At the moment it’s possible to only open 1 account in € and 1 in each other currency. The savings accounts don’t have their own IBAN either. Their savings acts like a fund."
            f"Write a review at the level of a community college graduate using the tone, structure, and style of the examples above. Maintain the conversational, informal tone, and include natural errors, such as missing articles, incorrect prepositions, and some common conversational phrases like 'you know', 'like', 'honestly'. Use a friendly and personal voice, and make sure the review sounds casual and approachable. Such as:\n"
            f" - Unfinished thoughts: Start a thought and leave it hanging like 'I mean, it's just… you know?' or 'It's good but like…'\n"
            f" - Repeated punctuation**: Use repeated punctuation, like '!' or '?' multiple times in a row (e.g., 'It’s amazing!!!', 'I love it???').\n"
            f" - Nonsensical or illogical phrases: Throw in phrases that don’t quite make sense or are unusual, like 'I totally dig it, you know what I mean?' or 'It’s so cool, like, really cool... yeah'.\n"
            f" - Grammar mistakes: Introduce subtle grammar mistakes, such as: omitting articles (e.g., 'went to store'), wrong prepositions (e.g., 'in the bus' instead of 'on the bus'), or swapped words (e.g., 'definately' instead of 'definitely').\n"
            f" - Repetition of words: Repeat words unnecessarily for emphasis, like 'I really, really like it' or 'It’s like super, super good.'\n"
            f" - Overuse of colloquial language: Include excessive use of 'like', 'you know', 'actually', 'well', etc.\n"
            f" - Random spacing and indentations: Add random spaces before or after punctuation or between words. You can also add extra spaces between sentences or paragraphs.\n"
            f" - Line breaks and random sentence splitting: Occasionally break up a sentence into two lines, or start a new line halfway through a sentence to mimic casual writing habits.\n"
            f" - Include incomplete sentences or unfinished thoughts: People sometimes don’t finish their sentences or thoughts. For example: 'It’s good, but... well, not exactly what I thought.'\n"
            f" - Emotional or subjective commentary: Use subjective statements like 'I mean, I totally love it, but like... it could be better' or 'Honestly, it's not bad, but I guess I expected more.'\n"
            f" - Slight illogical jumps: Include transitions that feel random or slightly off-topic, such as 'But then again, you know what I mean?' or 'Honestly, I didn’t expect that to happen.'\n"
            f" - Break text into new lines for no reason: Randomly break text into a new line or a sentence midway for a more disjointed feel.\n"
            f"Then, rewrite the following text in this style: {input_text}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1.3,
            frequency_penalty=0.4,
            presence_penalty=0.7,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "review_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "review": {
                                "description": "A rewritten version of the text that feels human-like and casual.",
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


def translate_text(input_text, language):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a language translator assistant"},
                {"role": "user", "content": f"Translate the following text into {language}: {input_text}"},
            ],
            temperature=1.3,
            frequency_penalty=0.4,
            presence_penalty=0.7,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "text_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "description": "The translated text",
                                "type": "string",
                            },
                        }
                    },
                }
            }
        )

        content = response.choices[0].message.content
        json_content = json.loads(content)
        return json_content.get("text", "No review found.")
    except Exception as e:
        raise RuntimeError(f"OpenAI request failed: {e}")