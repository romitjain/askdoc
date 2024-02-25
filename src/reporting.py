import sys
import pytesseract
from typing import Dict
from loguru import logger
from pdf2image import convert_from_path

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

class ReportParser():
    def __init__(self) -> None:
        self.image_ocr = {}

    def __call__(self, filename: str) -> Dict:
        """
        Processes the report and returns
        a JSON object of all the elements in the report
        """

        self.images = convert_from_path(filename)

        for idx, image in enumerate(self.images):
            logger.info(f'Processing page number {idx} of the PDF')

            text: str = pytesseract.image_to_string(image)
            text = text.strip()
            self.image_ocr.update({idx: text})

        return self.image_ocr

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='Filepath of the report')

    args = parser.parse_args()

    parser = ReportParser()
    parsed_report = parser(filename=args.f)

    for k, v in parsed_report.items():
        print(v)
        print('\n')
