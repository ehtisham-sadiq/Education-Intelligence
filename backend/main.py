from fastapi import FastAPI
from transformers import pipeline


app = FastAPI()
pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
@app.get("/")
async def root(name:str = None):
    if name:
        return {"message": f"Hello {name}"}
    return {"message": "Hello World"}


# create a end-point to convert text to speech
@app.get("/text-to-speech")
async def text_to_speech(text:str):
    # convert text to speech
    speech = pipe(text)
    # save the speech to a file
    # return the speech
    return {"message": f"Text to speech: {speech}"}


