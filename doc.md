# AskDoc

user flow
    - ask for a medical-related question
    - wants to understand the medicines
    - wants to book consultations

tech flow
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
