import textwrap

from main import constants
from app.gpt import gpt


def generate_summary(script_text: str):

    text = script_text
    max_cycle = int(len(text) / constants['chunk_size']['small']) + 1
    summary_prompt = constants['prompt']['summary']
    summary = ''

    for cycle in range(max_cycle):

        chunks = textwrap.wrap(text, constants['chunk_size']['small'])

        if len(chunks) == 1:
            summary = gpt.request_gpt(text + summary_prompt)
            break

        chunk_summaries = [gpt.request_gpt(chunk + summary_prompt) for chunk in chunks]
        summary = ' '.join(chunk_summaries)

        text = summary

    return summary
