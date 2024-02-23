import sys
import gradio as gr
from loguru import logger
from .engines import verify, medical

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

def respond(message, history):
    logger.debug(f'History: {history}')
    v = verify(message)
    logger.info(f'Is medical query: {v}')

    # If it is not a medical query, respond appropriately
    if v.lower() == 'no':
        return 'I can not help you with your query. Please keep your queries realted to medical context'

    return medical(message)

demo = gr.ChatInterface(respond)

if __name__ == "__main__":
    demo.launch()
