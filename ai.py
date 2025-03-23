from openai import OpenAI

def generate_content(prompt):

  api_key = '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'

  client = OpenAI(
      api_key=api_key
  )

  chat_completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
          {
              "role": "user",
              "content": prompt
          }
      ],
  )

  return chat_completion.choices[0].message.content