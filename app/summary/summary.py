import asyncio
import textwrap

from main import constants
from app.gpt import gpt


async def generate_summary(script_text: str, video_title: str):

    text = script_text
    max_cycle = int(len(text) / constants['chunk_size']['large']) + 1
    summary_prompt = constants['prompt']['summary']['kr']
    final_summary_prompt = constants['prompt']['final_summary']['en']
    summary = ''

    for cycle in range(max_cycle):
        chunks = textwrap.wrap(text, constants['chunk_size']['large'])

        if len(chunks) == 1:
            summary = await gpt.request_gpt(text + final_summary_prompt,
                                            constants['prompt']['final_summary']['system_message'])
            break

        tasks = [gpt.request_gpt(summary_prompt + "\n title : " + video_title + "\n script : " + chunk,
                                 constants['prompt']['summary']['system_message']) for idx, chunk in enumerate(chunks)]
        chunk_summaries = await asyncio.gather(*tasks)
        summary = ' '.join(chunk_summaries)

        text = summary

    return summary
