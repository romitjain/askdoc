# AskDoc

This bot understands your medical concerns and helps diagnose them. Here is what you can do:

1. Ask for your health-related questions.
2. Send a medical report and ask questions based on that

Under the hood, it is a:

1. ChatGPT
    - give GPT a personality prompt
    - validation of input
      - is it a medical question or not
      - can a health doc answer this
    - validation of output
      - should not be prescriptive of a drug
      - should be grounded somehow
    - if the user adds an attachment
      - parse the attachment
      - send it to GPT (OCR + Image)
    - memory
      - save abstraction of every 10 conversations in memory
      - save abstraction of attachments/reports
    - personalization
      - retrieve from memory during runtime for the user
