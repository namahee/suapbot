import requests
from bs4 import BeautifulSoup as bs
from pyrogram import filters
from pyrogram.types import Message
from .sql.sql import *
from suapbot import _login, discs, _notas, cmd
from client import b

@b.on_message(cmd("login"))
async def login(_, message: Message):
	if get_wait(message.from_user.id):
		remove_wait(message.from_user.id)
	if get_login(message.from_user.id):
		await message.reply("`Você já possui um login.`")
	else:
		await message.reply("`Digite seu usuário e senha dessa forma:\n\n[usuário] [senha]`")
		add_wait(message.from_user.id, "login")

@b.on_message(cmd("logout"))
async def logout(_, message: Message):
	if get_login(message.from_user.id):
		remove_login(message.from_user.id)
		await message.reply("`Logout efetuado!`")
	else:
		await message.reply("`Você não possui um login.`")
		
@b.on_message(cmd("boletim"))
async def boletim(_, message: Message):
    if get_wait(message.from_user.id):
	    remove_wait(message.from_user.id)
    if get_login(message.from_user.id):
    	username, senha = get_login(message.from_user.id)
    	if get_disc(message.from_user.id):
    		disciplinas = get_disc(message.from_user.id)
    	else:
    		discs(message.from_user.id, _login(username, senha))
    		disciplinas = get_disc(message.from_user.id)
    	#disciplinas, _, _ = get_disciplinas(_login(username, senha))
    	add_wait(message.from_user.id, "nota")
    	help_text = f"`Escolha a disciplina:\n{disciplinas}`"
    	return await message.reply(help_text, quote=True)
    else:
    	return await message.reply("`Você não possui um login. Utilize o comando /login para criar.`")


@b.on_message(filters.private)
async def pera(_, message: Message):
	if get_wait(message.from_user.id):
		if get_for(message.from_user.id) == "login":
			try:
				username, password = message.text.split(" ")
			except:
				await message.reply("`Digite as crendenciais corretamente.`")
			else:
				vc = await message.reply("`Verificando credenciais...`")
				if _login(username, password):
					add_login(message.from_user.id, username, password)
					await vc.edit("`Login efetuado!`")
					remove_wait(message.from_user.id)
				else:
					await vc.edit("`Usuário ou senha inválido. Digite novamente.`")
			
		if get_for(message.from_user.id) == "nota":
			username, password = get_login(message.from_user.id)
			_, disc, disciplinas = discs(message.from_user.id, _login(username, password))
			#if (message.text).lower() != "stop":
				
			if int(message.text) >= 1 and int(message.text) <= len(list(disciplinas)):
				#remove_wait(message.from_user.id)
				disciplina_escolhida = disciplinas[int(message.text) - 1]
				print("AQUI: "+disciplina_escolhida)
				boletim = _notas(disciplina_escolhida, disc)
				await message.reply(boletim)
			else:
				await message.reply("`Selecione um número correto.`")
			#else:
				#remove_wait(message.from_user.id)

