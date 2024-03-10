from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def create_client_instance():
    """Get .env key for the api, create client object with OpenAI and return the client object"""
    api_key = os.getenv("OPENAI_KEY")
    print(api_key)
    client = OpenAI(api_key=api_key)
    return client


def make_request(client, model="gpt-3.5-turbo", messages=None, temperature=0):
    """Accepts a client connection with OpenAI as well as the model type, message list/array containing user and
    content, and temperature"""
    MODEL = model
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content