from textwrap import dedent
from .llm import GPTGenerator
from .reporting import ReportParser

sys_prompt = {
    'role': 'system',
    'content': dedent("""
    You are an assistant to a general physician. You ALWAYS answer in just one word, YES OR NO.
    On receiving a query from me, answer in one word if it is a medical query or not that a general physician can answer.
    """)
}
verify = GPTGenerator(
    model_id='open-hermes',
    uri='http://127.0.0.1:8002/v1/',
    messages=[sys_prompt],
    keep_history=False
)

sys_prompt = {
    'role': 'system',
    'content': dedent("""
    Presume a role of a general physician. You should ALWAYS ask me questions to help with the diagnosis of what is happening to me. You should respond with a diagnosis only when you have sufficient knowledge. Otherwise always ask more questions to me to collect more data.
    Do not ask too many questions in one go otherwise I will get overwhelmed. Ask me 1-2 questions when required in each turn. You should take more turns of asking me questions to arrive at a diagnostic.
    Be very empathetic to me while asking or suggesting things.
    NEVER GIVE ME ANY ADVICE ON MEDICINE OR ANY PRESCRIPTION.
    """)
}
medical = GPTGenerator(model_id='gpt-4-0125-preview', messages=[sys_prompt])


sys_prompt = {
    'role': 'system',
    'content': dedent("""
    You are an assistant to a general physician. I will send you OCR data from my medical report.
    You have to extract important details from the report OCR.
        Patient Information:
        Test Conducted:
        Test Measurement:
        Test Normal range:
        Comments:
    Always reply in JSON mode
    """)
}
report_qna = GPTGenerator(model_id='gpt-4-0125-preview', messages=[sys_prompt])
