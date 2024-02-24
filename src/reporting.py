import re
import sys
import pytesseract
from typing import Dict
from loguru import logger
from pdf2image import convert_from_path
from transformers import DonutProcessor, VisionEncoderDecoderModel

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

class ReportParser():
    def __init__(self) -> None:
        self.processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
        self.model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

        self.model.to('cuda:0')

    def __call__(self, filename: str) -> Dict:
        """
        Processes the report and returns
        a JSON object of all the elements in the report

        Args:
            filename (str): _description_
        """
        images = convert_from_path(filename)

        image_ocr = {}

        for idx, image in enumerate(images):
            logger.info(f'Processing {idx} page of the PDF')
            # prepare decoder inputs
            task_prompt = "<s_cord-v2>"
            decoder_input_ids = self.processor.tokenizer(
                task_prompt, add_special_tokens=False, return_tensors="pt"
            ).input_ids

            pixel_values = self.processor(image, return_tensors="pt").pixel_values

            outputs = self.model.generate(
                pixel_values.to('cuda:0'),
                decoder_input_ids=decoder_input_ids.to('cuda:0'),
                max_length=self.model.decoder.config.max_position_embeddings,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True,
                bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
            )

            sequence = self.processor.batch_decode(outputs.sequences)[0]
            sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(
                self.processor.tokenizer.pad_token, "")

            sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()

            image_ocr.update({idx: sequence})

        return image_ocr

    def alt(self, filename: str) -> Dict:
        """
        Processes the report and returns
        a JSON object of all the elements in the report

        Args:
            filename (str): _description_
        """
        images = convert_from_path(filename)

        image_ocr = {}

        for idx, image in enumerate(images):
            logger.info(f'Processing {idx} page of the PDF')
            # prepare decoder inputs
            text: str = pytesseract.image_to_string(image, output_type=pytesseract.Output.DICT)
            text = text.strip()
            image_ocr.update({idx: text})

        return image_ocr

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='Filepath of the report')

    args = parser.parse_args()

    report = ReportParser()

    parsed_report = report.alt(filename=args.f)

    print(parsed_report)
