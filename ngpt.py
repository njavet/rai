import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'),)

def get_comp():
    chat_comp = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': 'does god exist?',
                    }
                ],
            model='gpt-3.5-turbo',
            )
    return chat_comp

