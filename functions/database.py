import json
import random

file_name = "store.json"


def get_recent_messages():
    learn_instruction = {
        "role": "system",
        "content": "You are a Spanish teacher and your name is Rachel, the user is called Shaun. Keep responses under 20 words.",
    }

    messages = []

    x = random.uniform(0, 1)

    if x < 0.2:
        learn_instruction["content"] = (
            learn_instruction["content"] + "Your response will have some light humour. "
        )
    elif x < 0.5:
        learn_instruction["content"] = (
            learn_instruction["content"]
            + "Your response will include an interesting new fact about Spain."
        )
    else:
        learn_instruction["content"] = (
            learn_instruction["content"]
            + "Your response will recommend another word to learn. "
        )

    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except:
        pass

    return messages


def store_messages(request_message: str, response_message: str):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "system", "content": response_message}

    messages.append(user_message)
    messages.append(assistant_message)

    with open(file_name, "w") as f:
        json.dump(messages, f)


def reset_messages():
    open(file_name, "w")
