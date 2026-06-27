from fastapi import FastAPI

app = FastAPI(title = "RelayFlow ")

@app.get("/")
async def root():
    return {"message": "Up and running!"}
