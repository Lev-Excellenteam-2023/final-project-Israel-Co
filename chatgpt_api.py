from typing import List, Tuple, Dict

import openai
import parsed_presentation

API_KEY = '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'


# function to generate text to be used in the chatbot
def generate_explain_to_slide(slide_text: str) -> str:
    """
    Generate explain from chatGPT
    :param slide_text: Text of the slide
    :return: Explain from chatGPT for slide's text
    """
    openai.api_key = API_KEY

    if len(slide_text.split()) < 10:
        return slide_text
    else:
        messages = [{'role': 'system', 'content': 'You are a great powerpoint lecture explainer!'},
                    {'role': 'user', 'content': slide_text}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content


def presentation_explainer(presentation: parsed_presentation.PresentationParser) -> List[str]:
    """
    Generate explain for each slide in the presentation
    :param presentation: Presentation to explain
    :return: List of explains for each slide in the presentation
    """
    explains_list = [''] * presentation.get_num_of_slides()

    for slide_num, slide_text in presentation.get_slide():
        explain = generate_explain_to_slide(slide_text)
        explains_list[slide_num] = explain

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
