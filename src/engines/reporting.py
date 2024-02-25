import sys
import pytesseract
from textwrap import dedent
from typing import Dict
from loguru import logger
from pdf2image import convert_from_path

from .llm import GPTGenerator
from src.utils import log_time

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

class ReportParser():
    def __init__(self) -> None:
        pass

    @log_time('report_parser')
    def __call__(self, filename: str) -> Dict:
        """
        Processes the report and returns
        a JSON object of all the elements in the report
        """
        image_ocr = {}

        self.images = convert_from_path(filename)

        for idx, image in enumerate(self.images):
            logger.info(f'Processing page number {idx} of the PDF')

            text: str = pytesseract.image_to_string(image)
            text = text.strip()
            image_ocr.update({idx: text})

        return image_ocr

    @log_time('clean_ocr')
    def clean_ocr(self, ocr: Dict) -> Dict:
        sys_prompt = {
            'role': 'system',
            'content': dedent("""
            Assume the role of an assistant to a general physician.
            I will send you OCR data from my medical report.
            You have to extract important details from the report OCR.
                Patient Information:
                Test Conducted:
                Test Measurement:
                Test Normal range:
                Comments:
            Always reply in JSON mode
            """)
        }

        report_cleaner = GPTGenerator(model_id='gpt-4-0125-preview', messages=[sys_prompt], keep_history=False)

        cleaned_ocr = {}
        for idx, ocr in ocr.items():
            cleaned_ocr.update({idx: report_cleaner(ocr, json_mode=True)})

        return cleaned_ocr

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
