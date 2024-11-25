from .client import b
from fastapi import FastAPI

app = FastAPI()
s = False

@app.on_event("startup")
async def start_bot():
    s = True
    print("Iniciando o bot...")
    await b.start()

@app.on_event("shutdown")
async def stop_bot():
    print("Parando o bot...")
    await b.stop()

@app.get("/")
def read_root():
    return {"message": "Bot Pyrogram está rodando no Vercel!"}

@app.get("/s")
def ss():
    return {"status": s}
