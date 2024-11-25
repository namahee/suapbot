from .client import b
from fastapi import FastAPI

app = FastAPI()
s = False

@app.on_event("startup")
async def start_bot():
    global s
    s = True
    print("Iniciando o bot...")
    await b.run()

@app.get("/")
def read_root():
    return {"message": "Bot Pyrogram está rodando no Vercel!"}

@app.get("/s")
def ss():
    b.run()
    return {"status": s}
