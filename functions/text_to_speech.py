from decouple import config
import requests

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


def convert_text_to_speech(message: str):
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
        },
    }

    voice_shaun = "mTSvIrm2hmcnOvb21nW2"
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"
    voice_antoni = "ErXwobaYiN019PkySvjV"

    headers = {
        "xi_api_key": ELEVEN_LABS_API_KEY,
        "content-type": "application/json",
        "accept": "audio/mpeg",
    }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return

    if response.status_code == 200:
        return response.content
    else:
        return
