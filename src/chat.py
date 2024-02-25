import sys
import gradio as gr
from loguru import logger
from .engines import verify, medical, report_qna, ReportParser

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

def respond(message, history, file):
    logger.debug(f'History: {history}')
    v = verify(message)
    logger.info(f'Is medical query: {v}')

    # If it is not a medical query, respond appropriately
    if v.lower() == 'no':
        return 'I can not help you with your query. Please keep your queries realted to medical context'

    # If a file is provided, process the file for further QnA
    if file:
        logger.info(f'Parsing the data in the file" {file}')
        try:
            parser = ReportParser()
            parsed_report = parser(file)
        except Exception as err:
            raise IOError(f'Not able to parse the file: {err}. Make sure the file is a PDF')

        # Add to memory

        # Query match message to the medical report, extract and then send to medical
        medical_report = []
        for idx, ocr in parsed_report.items():
            medical_report.append(
                report_qna(ocr, json_mode=True)
            )

    return medical(message)

demo = gr.ChatInterface(respond, additional_inputs=gr.File(label="Upload a medical report"))

if __name__ == "__main__":
    demo.launch()
