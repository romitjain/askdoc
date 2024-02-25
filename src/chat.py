import sys
import gradio as gr
from loguru import logger
from .generators import verify, medical
from .engines import ReportParser, UserMemory

memory = UserMemory()

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
            cleaned_report = parser.clean_ocr(parsed_report)
        except Exception as err:
            raise IOError(f'Not able to parse the file: {err}. Make sure the file is a PDF')

        # Add to memory
        memory.add_memory(
            documents=list(cleaned_report.values()),
            metadata=[
                f'Medical document, page: {k}' for k in cleaned_report.keys()]
        )

    # Query match message to the medical report, extract and then send to medical
    relevant_msg = memory.search(message)
    logger.info(f'Found relevant messages: {relevant_msg}')

    if relevant_msg:
        return medical(f'Context: {relevant_msg}\nQuery: {message}')

    return medical(message)

demo = gr.ChatInterface(respond, additional_inputs=gr.File(label="Upload a medical report"))

if __name__ == "__main__":
    demo.launch()
