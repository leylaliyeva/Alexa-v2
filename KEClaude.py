import anthropic

client = anthropic.Anthropic(api_key="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")


def ke(text):
  conversation=[]
  conversation.append({"role": "user", "content": text})
  response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=conversation
  )
        
  claude_response = response.content[0].text
  return claude_response

if __name__ == "__main__":
  t = "What is the melting point of silver?"
  u = ke(t)
  if u != None: print(u)
