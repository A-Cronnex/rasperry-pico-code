from fastapi import FastAPI

app = FastAPI()

stored_data = {}

@app.get("/")
async def root():
    return {"message: Hello World"}

@app.get("/api/command")
async def getCommand():
    return {"command":stored_data["command"]}

@app.post("/api")
async def postToRecord(command):
    global stored_data
    stored_data["command"] = command.command
    return {"status": "Got it!"}


