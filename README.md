# AskDoc

This bot understands your medical concerns and helps diagnose them. Here is what you can do:

1. Ask for your health-related questions
2. Send a medical report and ask questions based on that

This bot remembers information about you and considers that while conversing. It is also an empathetic bot and asks you relevant questions only.
This bot will require your OPENAI_API_KEY to work.

## Components

1. **Medical agent**: This is given a prompt to act like a doctor and do diagnostics. Currently, this is ChatGPT (Vision)
2. **Tesseract**: To extract information from PDF and image reports
3. **Validation agent** (Coming soon): This validates input/output
4. **Memory**: This memory is queried for relevant context when the user asks for a query
5. **Summarizer**: This summarizes the conversation after a certain number of turns and stores that summary in the memory for later retrieval

## Setup

### Create a new virtualenv

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### Install the package

```bash
pip install askdoc
export OPENAI_API_KEY=<openai API key>
```

### Run the command

```bash
# This will open a local webserver where you can chat. The link will be shown after the command
# and will look something like: HTTP://127.0.0.1:7860
askdoc
```
