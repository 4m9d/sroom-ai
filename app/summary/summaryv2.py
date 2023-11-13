import asyncio
import datetime
import re

from main import constants
from app.gpt import gpt


async def generate_summary(scripts: dict, video_title: str):
    time_stamp, chunks = divide_chunk(scripts)
    summary_prompt = constants['prompt']['final_summary']['kr']

    tasks = [gpt.request_gpt(summary_prompt + "\n script : " + chunk,
                             constants['prompt']['final_summary']['system_message']) for idx, chunk in enumerate(chunks)]

    summaries = await asyncio.gather(*tasks)

    final_summary = ''
    for idx, summary in enumerate(summaries):
        time_delta = datetime.timedelta(seconds=int(time_stamp[idx]))
        time_format = str(time_delta)
        final_summary += ('<button id=\"' + time_format.replace(":", "") + '\" class=\"timestamp\" style=\"'
                                        'color:#FA5B3E;font-size: 1.125rem;line-height: 1.75rem;text-decoration-line:none;'
                                        'display:inline-block;background-color:rgba(250, 91, 62, 0.2);border-radius:0.25rem;padding:0.125rem 0.25rem;\">' +
                          time_format + '</button>' + '\n')
        final_summary += summary + '\n \n '

    final_summary = reformat_summary(final_summary)
    return final_summary, summaries


def divide_chunk(scripts: dict):

    chunk_text = ''
    time_stamp = 0

    time_stamps = []
    chunks = []
    for script in scripts:
        if len(chunk_text) > 3000:
            chunk_text.replace("[음악]", "")
            chunk_text.replace("[박수]", "")
            chunks.append(chunk_text)
            time_stamps.append(time_stamp)
            time_stamp = script['start']
            chunk_text = script['text'] + ' '
        else:
            chunk_text += script['text']

    if len(chunk_text) < 1000 and len(chunks) > 0:
        chunks[-1] += chunk_text
    else:
        time_stamps.append(time_stamp)
        chunks.append(chunk_text)

    return time_stamps, chunks


def reformat_summary(summary: str):
    summary.replace("\#", "#")
    summary = re.sub(r"```", "", summary)
    return summary
