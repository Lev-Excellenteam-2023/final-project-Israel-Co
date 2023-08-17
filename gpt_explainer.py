import asyncio
import json
import os
from typing import List

from chatgpt_api import presentation_explainer
from parsed_presentation import PresentationParser


def store_explains(explained_slides_list: List[str], file_name: str):
    explained_slides_dict = [{"Slide_num: ": index + 1, 'Explain: ': explain}
                             for index, explain in enumerate(explained_slides_list)]
    with open(file_name, 'w') as jason_file:
        json.dump(explained_slides_dict, jason_file, indent=4)


async def main():
    file_path = input('Enter pptx file path: ')
    presentation = PresentationParser(file_path)
    explained_slides_list = await presentation_explainer(presentation)
    json_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.json'
    store_explains(explained_slides_list, json_file_name)


if __name__ == '__main__':
    asyncio.run(main())

