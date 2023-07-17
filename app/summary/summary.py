import textwrap

from main import constants
from app.script.script import *
from app.gpt.gpt import *


def generate_summary(script_text: str):

    text = script_text
    summary_prompt = constants['prompt']['summary']
    chunk_size = 3000
    summary = ""

    while True:

        chunks = textwrap.wrap(text, chunk_size)
        chunk_summaries = []

        if len(chunks) > 1:

            for chunk in chunks:
                chunk_summaries.append(request_gpt(chunk + summary_prompt))

            summary = " ".join(chunk_summaries)

            if len(chunks) > 3:
                text = summary
                continue

            summary = request_gpt(summary)

        else:
            summary = request_gpt(chunks[0])

        break

    return summary

