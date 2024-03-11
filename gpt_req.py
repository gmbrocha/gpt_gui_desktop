import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def create_client_instance():
    """Get .env key for the api, create client object with OpenAI and return the client object"""
    api_key = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=api_key)
    return client


def make_request(client, model="gpt-3.5-turbo", messages=None, temperature=0):
    """Accepts a client connection with OpenAI as well as the model type, message list/array containing user and
    content, and temperature"""
    MODEL = model
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
        )
    except openai.APIConnectionError as e:
        print(f"Server con error {e.__cause__}")
        raise
    except openai.RateLimitError as e:
        print(f"Rate limit error {e.status_code}: (e.response)")
    except openai.APIStatusError as e:
        print(f"OpenAI STATUS error {e.status_code}: (e.response)")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    return response.choices[0].message.content
