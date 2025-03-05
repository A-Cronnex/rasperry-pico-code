from fastapi import FastAPI

app = FastAPI()

stored_data = "sample"

@app.get("/")
async def root():
    return {"message: Hello World"}

@app.get("/command/")
async def getCommand():
    return {"command":stored_data}

@app.post("/api/")
async def postToRecord(command):
    global stored_data
    stored_data = command.command
    return {"status": "Got it!"}


