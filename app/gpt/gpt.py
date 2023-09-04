import aiohttp
import openai
import os

from main import constants

openai.api_key = os.environ['GPT_API_KEY']


async def request_gpt(prompt: str):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post(
            constants['model_parameter']['url'],
            headers={'Authorization': f'Bearer {openai.api_key}'},
            json={
                'messages': [
                    constants['prompt']['system_message'],
                    {"role": "user", "content": prompt}
                ],
                'model': constants['gpt_model']['small'],
                'temperature': constants['model_parameter']['temperature']['high'],
                'max_tokens': constants['model_parameter']['max_token']['1k']
            }
        ) as response:
            response_data = await response.json()
            return response_data["choices"][0]["message"]["content"]
