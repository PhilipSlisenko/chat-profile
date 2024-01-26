import os

from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2+2?"},
    ],
)


print(completion.choices[0].message.content)
