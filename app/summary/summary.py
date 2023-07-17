import textwrap

from main import constants
from app.script.script import *
from app.gpt.gpt import *


def generate_summary(script_text: str):

    summary_prompt = constants['prompt']['summary']
    chunk_size = 3000

    chunks = textwrap.wrap(script_text, chunk_size)
    chunk_summaries = []

    for chunk in chunks:
        chunk_summaries.append(request_gpt(chunk + summary_prompt))

    summary = " ".join(chunk_summaries)

    if len(chunks) > 3:
        return generate_summary(summary)
    elif len(chunks) > 1:
        summary = request_gpt(summary)

    summary = reformat_summary(summary)

    return summary


def reformat_summary(summary: str):
    summary = summary.replace("\n", "\\n")
    summary = summary.replace("\"", "\\\"")

    return summary
