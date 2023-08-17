import asyncio
from typing import List, Tuple, Dict

import openai

import openAI_key
import parsed_presentation


async def generate_explain_for_slide(slide_text: str, secret_key: openai.api_key) -> Tuple[int, str]:
    """
    Generate explain from chatGPT
    :param secret_key: Secret key for openAI
    :param slide_text: Text of the slide
    :return: Explain from chatGPT for slide's text
    """
    openai.api_key = secret_key

    if len(slide_text.split()) < 10:
        return slide_text
    else:
        messages = [{'role': 'system',
                     'content': 'You are a great powerpoint explainer! and you have to explain the slide in about 100 words'},
                    {'role': 'user', 'content': slide_text}]
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content


async def presentation_explainer(presentation: parsed_presentation.PresentationParser) -> List[str]:
    """
    Generate explain for each slide in the presentation
    :param presentation: Presentation to explain
    :return: List of explains for each slide in the presentation
    """
    explains = await asyncio.gather(
        *(generate_explain_for_slide(slide_text, openAI_key.API_KEY) for slide_num, slide_text in
          presentation.get_slide()))

    return explains
