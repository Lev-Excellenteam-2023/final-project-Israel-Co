from pptx import Presentation
import re
from typing import List, Tuple


class PresentationParser:
    """
    Parsed presentation. Extracting each slide text and gathering them by subject(title).
    """

    def __init__(self, path: str):
        """
        constructor
        :param path: Path of presentation file
        """
        self._slide_counter = 0
        self._presentation_subjects = {}
        self._parse_presentation(path)

    def _parse_presentation(self, path: str):
        """
        Parse the presentation. Extract the text from each slide and save it by subject.
        :param path: Path of presentation file
        :return: Parsed presentation divided into a dictionary, the Key is slides title and the value is list of tuples.
                 Each tuple contains the slide number and the text slide.
                 e.g. {Title1: [(1, '1st slide text), (2, 2nd slide text)], Title2: [(3, '3rd slide text)], ... }
        """
        presentation = Presentation(path)
        for slide in presentation.slides:
            slide_title = slide.shapes.title.text
            slide_text = self._extract_text_from_slide(slide)

            if slide_title in self._presentation_subjects:
                self._presentation_subjects[slide_title] += [(self._slide_counter, slide_text)]
            else:
                self._presentation_subjects[slide_title] = [(self._slide_counter, slide_text)]

            self._slide_counter += 1

    def _extract_text_from_slide(self, slide) -> str:
        """
        Extract text from the slide
        :param slide:
        :return:
        """
        slide_text_list = []
        slide_text_list += [shape.text + '\n' for shape in slide.shapes if hasattr(shape, 'text')]
        slide_text = ''.join(slide_text_list)

        return clean_weird_whitespaces(slide_text)

    def get_section(self) -> Tuple[str, List[Tuple[int, str]]]:
        """
        Generator which returns list of tuples. Each tuple contains slide number and the text slide.
        e.g. [(1, '1st slide text), (2, 2nd slide text)]
        :return: Generator that gives tuple of subject and list of tuples.
        Each tuple contains slide number and the text slide.
        """
        for subject in self._presentation_subjects:
            yield subject, self._presentation_subjects[subject]


def clean_weird_whitespaces(text: str) -> str:
    """
    Clean weird whitespaces likewise two spaces, tabs est.
    :param text: Text to clean
    :return: The cleaned text
    """
    text = re.sub('^\n+', '', text)
    text = re.sub('\n\n+', '\n', text)
    text = re.sub('  +', ' ', text)
    text = re.sub('\t\t+', '\t', text)
    return text


# if __name__ == '__main__':
#     prs = PresentationParser(r'C:\Users\josh5\Downloads\ogging, debugging, getting into a large codebase.pptx')
#     for section, slides in prs.get_section():
#         print(section)
#         for slide in slides:
#             print(f'\t{slide[0]}: {slide[1]}')
