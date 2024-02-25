from textwrap import dedent
from .engines import GPTGenerator

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
    Presume the role of a general physician. You should ALWAYS ask me questions to help with the diagnosis of what is happening to me. You should respond with a diagnosis only when you have sufficient knowledge. Otherwise always ask me more questions to collect more data about my condition.
    Do not ask too many questions in one go otherwise I will get overwhelmed. Ask me 1-2 questions when required in each turn. You should take more turns asking me questions to arrive at a diagnostic.
    Be very empathetic to me while asking or suggesting things.
    I might provide some context from my medical reports. You can choose to use that context to personalize your response.
    NEVER GIVE ME ANY ADVICE ON MEDICINE OR ANY PRESCRIPTION.
    """)
}
medical = GPTGenerator(model_id='gpt-4-0125-preview', messages=[sys_prompt])

