import asyncio
from typing import List, Tuple, Dict

import openai

import openAI_key
import parsed_presentation


async def generate_explain_for_slide(slide_number: int, slide_text: str) -> Tuple[int, str]:
    """
    Generate explain from chatGPT
    :param slide_number: Number of the slide
    :param slide_text: Text of the slide
    :return: Explain from chatGPT for slide's text
    """
    openai.api_key = openAI_key.API_KEY

    if len(slide_text.split()) < 10:
        return slide_number, slide_text
    else:
        messages = [{'role': 'system',
                     'content': 'You are a great powerpoint explainer! and you have to explain the slide in about 100 words'},
                    {'role': 'user', 'content': slide_text}]
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return slide_number, response.choices[0].message.content


async def presentation_explainer(presentation: parsed_presentation.PresentationParser) -> List[str]:
    """
    Generate explain for each slide in the presentation
    :param presentation: Presentation to explain
    :return: List of explains for each slide in the presentation
    """
    explains_list = [''] * presentation.get_num_of_slides()

    explains = await asyncio.gather(
        *(generate_explain_for_slide(slide_num, slide_text) for slide_num, slide_text in presentation.get_slide()))

    for index, explain in explains:
        explains_list[index] = explain

    return explains_list

# def main():
#     prs = parsed_presentation.PresentationParser(
#         # r'C:\Users\josh5\Downloads\asyncio-intro (1).pptx')
#         r'C:\Users\josh5\Downloads\ogging, debugging, getting into a large codebase.pptx')
#     list_explained = presentation_explainer(prs)
#     for slide_num in range(len(list_explained)):
#         print(f'{slide_num}:', list_explained[slide_num])
#
#
# if __name__ == '__main__':
#     main()
