import asyncio

import aiohttp
import openai
import os

from main import constants

openai.api_key = os.environ['GPT_API_KEY']

MAX_CYCLE = 30


async def request_gpt(prompt: str, system_message: dict):

    for cycle in range(MAX_CYCLE):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.post(
                    constants['model_parameter']['url'],
                    headers={'Authorization': f'Bearer {openai.api_key}'},
                    json={
                        'messages': [
                            system_message,
                            {"role": "user", "content": prompt}
                        ],
                        'model': constants['gpt_model']['large'],
                        'temperature': constants['model_parameter']['temperature']['high'],
                        'max_tokens': constants['model_parameter']['max_token']['2k']
                    }
                ) as response:
                    response_data = await response.json()
                    print(response.status)

                    if response.status == 200:
                        return response_data["choices"][0]["message"]["content"]
                    elif response.status == 429:
                        print("exceed GPT rate limit. wait for 10 sec")
                        await asyncio.sleep(10)
                    elif response.status == 500 or response.status == 503:
                        print('GPT Server Error. wait for 30 sec')
                        await asyncio.sleep(30)
            except:
                print("etc Error retry")

    raise Exception('GPT rate limit retry failed')
