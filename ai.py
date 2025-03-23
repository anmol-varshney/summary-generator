from openai import OpenAI
import streamlit as st

def generate_content(prompt):

  api_key = st.secrets["openai"]["api_key"]

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