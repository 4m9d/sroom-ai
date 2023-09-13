import asyncio
import textwrap

from main import constants
from app.gpt import gpt


async def generate_summary(script_text: str):

    text = script_text
    max_cycle = int(len(text) / constants['chunk_size']['large']) + 1
    summary_prompt = constants['prompt']['summary']
    final_summary_prompt = constants['prompt']['final_summary']
    summary = ''

    for cycle in range(max_cycle):
        chunks = textwrap.wrap(text, constants['chunk_size']['large'])

        if len(chunks) == 1:
            summary = await gpt.request_gpt(text + final_summary_prompt)
            break

        tasks = [gpt.request_gpt(chunk + summary_prompt) for idx, chunk in enumerate(chunks)]
        chunk_summaries = await asyncio.gather(*tasks)
        summary = ' '.join(chunk_summaries)

        text = summary

    return summary
