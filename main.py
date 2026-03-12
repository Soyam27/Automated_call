from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
import requests
app = FastAPI()
count = 0

@app.post("/voice")
async def voice():
    global count
    resp = VoiceResponse()
    if(count==0):
        resp.say("Good morning! I am your AI Call Assistant, Ask me anything:");
    else:
        resp.say("Ask me next question!")

    count = count+1
    gather = resp.gather(
        input="speech",
        action="/process",
        method="POST",
        speechTimeout="1",   
        timeout=3            
    )

    return Response(content=str(resp), media_type="application/xml")


@app.post("/process")
async def process(request: Request):
    form = await request.form()
    speech = form.get("SpeechResult")
    prompt = "answer eveything strictly with in 20-25 words "+ speech

    print("Caller said:", speech)
    

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    )

    data = response.json()

    print("AI Says: " + data["response"])


    resp = VoiceResponse()
    resp.say(data["response"])

    resp.redirect("/voice", method="POST")

    return Response(content=str(resp), media_type="application/xml")