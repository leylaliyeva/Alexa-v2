import google.generativeai as genai

API_KEY = 'AIzaSyByWQKHk-xZsu8Rg_kXaEZnPviNHFIj9_g'

# Endpoint for generating text
ENDPOINT = "https://language.googleapis.com/v1beta1/projects/-/locations/global/models/gemini-pro:generateText"
genai.configure(api_key=API_KEY)

def ke(prompt):
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  response = chat_session.send_message(prompt)

    
  return response.text

if __name__ == "__main__":
  t = "What is the melting point of silver?"
  u = ke(t)
  if u != None: print(u)

