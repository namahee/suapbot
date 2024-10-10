from pyrogram import Client

import os
import importlib

class Config:
    API_ID = int(3716600)# int(os.environ.get("API_ID"))
    API_HASH = str("0ed423ceea4fbb06c0e627d9db0f4a6b")# str(os.environ.get("API_HASH"))
    BOT_TOKEN = str("2023772023:AAELvE7PzeD2hggebtCuN0HM5FWhV9WbXgs")# str(os.environ.get("BOT_TOKEN"))

class Bot(Client):
    def __init__(self):
        kwargs = {
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'name': "bot",
            'bot_token': Config.BOT_TOKEN
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        print("START")
        try:
            path = os.listdir("suapbot/plugins")
            for p in path:
                if p.endswith(".py"):
                    arq = p.replace(".py", "")
                    importlib.import_module("plugins." + arq)
        except Exception as e:
            print(str(e))
            await self.send_message(1157759484, f"**❌ OCORREU UM ERRO**\n\nNão foi possível importar os plugins, ocorreu este erro: `{str(e)}`")
        else:
            await self.send_message(1157759484, "I'm on, man.`")

    async def stop(self):
        await super().stop()
        print("STOP")

b = Bot()


		
