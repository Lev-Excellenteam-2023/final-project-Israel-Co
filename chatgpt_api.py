from typing import List, Tuple, Dict

import openai
import parsed_presentation

API_KEY = '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'


# function to generate text to be used in the chatbot
def generate_response(title: str, presentation_subject: List[Tuple[int, str]]) -> Dict[int, str]:
    headline = 'Can you explain me this presentation?\n'

    openai.api_key = API_KEY

    slides_dict = {}

    for slide_number, slide_text in presentation_subject:
        if slide_text == title + '\n':
            response = slide_text
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{'role': 'user', 'content': headline + slide_text}]
            )
            # response = openai.Completion.create(
            #     engine="davinci",
            #     prompt=headline + slide_text
            # )
            headline = ''
            response = response.choices[0].message.content

        slides_dict[slide_number] = response

    return slides_dict


def main():
    prs = parsed_presentation.PresentationParser(
        r'C:\Users\josh5\Downloads\ogging, debugging, getting into a large codebase.pptx')
    for subject, slides in prs.get_section():
        exp = generate_response(subject, slides)
        for k in exp:
            print(exp[k])
        print('=' * 100)


if __name__ == '__main__':
    main()
