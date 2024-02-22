"""
Simple wrapper class around GPT API
"""
import sys
import json
import openai
import backoff

from typing import Tuple, Dict, List
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level='INFO')

add_assistant_msg_json = lambda x: {'role': 'assistant', 'content': json.dumps(x)}
add_usr_msg_json = lambda x: {'role': 'user', 'content': json.dumps(x)}
add_assistant_msg = lambda x: {'role': 'assistant', 'content': x}
add_usr_msg = lambda x: {'role': 'user', 'content': x}

class GPTGenerator():
    def __init__(self, model_id: str, messages: List=[], uri: str=None, keep_history: bool=True) -> None:
        from dotenv import load_dotenv
        load_dotenv()

        self.client = openai.OpenAI(base_url=uri)
        self.model_id = model_id
        self.messages = messages
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.keep_history = keep_history

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_time=300)
    def __call__(
        self,
        message: str,
        json_mode: bool = False,
        **kwargs
    ) -> str:

        message = add_usr_msg(message)

        if self.keep_history:
            self.messages.append(message)
            response = self._get_response(
                self.messages, json_mode, **kwargs
            )
            formatted_response = add_assistant_msg_json(response) if json_mode else add_assistant_msg(response)
            self.messages.append(formatted_response)

            return response

        message = self.messages + [message]
        response = self._get_response(
            message, json_mode, **kwargs
        )


    def _get_response(self, messages, json_mode, **kwargs) -> str:
        if json_mode:
            completions = self.client.chat.completions.create(
                model=self.model_id,
                response_format={'type': 'json_object'},
                messages=messages,
                **kwargs
            )

            if completions.choices[0].finish_reason == 'length':
                raise IOError(f'Reached maximum output length, output format is not reliable. {completions.choices[0].message.content}')

            op = json.loads(completions.choices[0].message.content)

        else:
            completions = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                **kwargs
            )

            op = completions.choices[0].message.content

        logger.debug(f'Prompts: {messages[-1]}, output: {op}')
        logger.debug(f'Tokens used in generation using {self.model_id}: {completions.usage}')

        self.total_tokens += completions.usage.total_tokens
        self.input_tokens += completions.usage.prompt_tokens
        self.output_tokens += completions.usage.completion_tokens

        return op
