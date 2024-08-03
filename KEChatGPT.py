import os
from flask import jsonify
from openai import OpenAI

api_key = 'sk-proj-AbezuJRS5txE67jw8YwJT3BlbkFJp6KLd7JuxyL3kuOSiR3b'

client = OpenAI(api_key=api_key)

def ke(text):

  completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": text,
        }
    ],
    model="gpt-3.5-turbo"
  )

  assistant_reply = completion.choices[0].message.content.strip()

  return assistant_reply
  # if rsp.status_code == 200:
  #   return rsp.text
  # else:
  #   return None

if __name__ == "__main__":
  t = "What is the melting point of silver?"
  u = ke(t)
  if u != None: print(u)
