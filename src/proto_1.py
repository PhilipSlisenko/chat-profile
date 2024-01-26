import json
import os
import pprint
from typing import List, TypedDict

from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"


client = OpenAI()


class DataRecord(TypedDict):
    username: str
    text: str
    timestamp: str


def get_data(
    file_path="/Users/philip/Documents/projects/kostya/chat-user-personality/data/Philip13579_dump.jsonl",
) -> List[DataRecord]:
    data: List[DataRecord] = []

    with open(file_path, "r") as file:
        for line in file:
            data.append(json.loads(line))

    return data


def get_chat_history_prompt_part(data):
    return json.dumps(
        sorted(data, key=lambda x: x["timestamp"]), indent=4, ensure_ascii=False
    )


def get_system_prompt(
    chat_history: str, current_message: str, current_profile: str
) -> str:
    sys_prompt = f'''
You are a psychology exprert who creates human profiles. You create them in JSON format. You will be presented with:
- chat history
- current mesage - the current message of a person of interest. based on this current message you will update profile.json
- current profile.json - previous (initial) state of profile.json that you will modify
You will reply with updated profile.json

CHAT_HISTORY"""
{chat_history}
"""

CURRENT_MESSAGE"""
{current_message}
"""

CURRENT_profile.json"""
{current_profile}
"""
'''
    return sys_prompt


def update_profile(
    current_profile: dict, chat_history: List[DataRecord], current_message: str
) -> dict:
    current_profile_str = json.dumps(current_profile, ensure_ascii=False, indent=4)
    chat_history_str = get_chat_history_prompt_part(chat_history)
    sys_prompt = get_system_prompt(
        chat_history_str, current_message, current_profile_str
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": sys_prompt},
        ],
        response_format={"type": "json_object"},
    )

    print(completion.choices[0].message.content)
    json_str = str(completion.choices[0].message.content)

    return json.loads(json_str)


def get_profile(chat_history: List[DataRecord], username: str):
    chat_history_prompt_part = get_chat_history_prompt_part(chat_history)
    current_message = ""
    current_profile: dict = {}
    for message in reversed(chat_history):
        if message["username"] != username:
            continue
        current_message = message["text"]
        current_profile = update_profile(current_profile, chat_history, current_message)


def main():
    data = get_data()
    get_profile(data, "ricata91")


if __name__ == "__main__":
    main()
