from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from functions.database import reset_messages, store_messages

from functions.openai_requests import convert_audio_to_text, get_chat_response


app = FastAPI()

origins = ["https://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def root():
    return {"message": "health"}


@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "reset"}


@app.get("/get-audio")
async def get_audio():
    audio_input = open("HELP!.wav", "rb")
    message_decorded = convert_audio_to_text(audio_input)
    print(message_decorded)
    return {"message": message_decorded}


@app.post("/post-audio/")
async def create_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:  # type: ignore
        buffer.write(file.file.read())

    audio_input = open(file.filename, "rb")  # type: ignore

    message_decoded = convert_audio_to_text(audio_input)

    if not message_decoded:
        raise HTTPException(status_code=400, detail="No message found")

    chat_response = get_chat_response(message_decoded)

    store_messages(message_decoded, chat_response)  # type: ignore

    audio_output = convert_audio_to_text(chat_response)
    if not audio_output:
        raise HTTPException(status_code=400, detail="No Audio found")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
