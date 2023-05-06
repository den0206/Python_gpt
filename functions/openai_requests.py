from decouple import config
import openai

from functions.database import get_recent_messages

openai.api_key = config("OPEN_AI_KEY")


def convert_audio_to_text(audio_file) -> str | None:
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text: str = transcript["text"]  # type: ignore
        return message_text
    except Exception as e:
        print(e)
        return


def get_chat_response(message_input: str) -> str | None:
    messages = get_recent_messages()
    user_message = {
        "role": "user",
        "content": message_input
        + " Only say two or 3 words in Spanish if speaking in Spanish. The remaining words should be in English",
    }
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        message_text: str = response["choices"][0]["message"]["content"]  # type: ignore
        return message_text
    except Exception as e:
        return
