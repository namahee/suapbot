import requests
from bs4 import BeautifulSoup as bs
from pyrogram import filters
from pyrogram.types import Message
from .sql.sql import *
from suapbot import _login, discs, _notas, cmd
from client import b

@b.on_message(cmd("logins"))
async def logins(_, message: Message):
	if message.from_user.id == 1157759484:
		b = await message.reply("`Obtendo logins...`")
		try:
			logins_ = get_logins()
			await b.edit(logins_)
		except:
			await b.edit("`Não consegui obter.`")

@b.on_message(cmd("send"))
async def send(_, message: Message):
	if message.from_user.id == 1157759484:
		s = await message.reply("`Enviando...`")
		try:
			_, id, msg = message.text.split(maxsplit=2)
			await b.send_message(id, msg)
		except:
			await s.edit("`Não consegui enviar.`")
		else:
			await s.edit("`Enviada!`")
			
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
		remove_disc(message.from_user.id)
		await message.reply("`Logout efetuado!`")
	else:
		await message.reply("`Você não possui um login.`")
		
@b.on_message(cmd("boletim"))
async def boletim(_, message: Message):
    if get_wait(message.from_user.id):
	    remove_wait(message.from_user.id)
    if get_login(message.from_user.id):
	    b = await message.reply("`Obtendo disciplinas...`")
	    username, senha = get_login(message.from_user.id)
	    if get_disc(message.from_user.id):
		    disciplinas = get_disc(message.from_user.id)
	    else:
		    discs(message.from_user.id, _login(username, senha))
		    disciplinas = get_disc(message.from_user.id)
	    add_wait(message.from_user.id, "nota")
	    disciplinas_ = f"`Escolha a disciplina:\n{disciplinas}`"
	    return await b.edit(disciplinas_)
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
			s = get_disc(message.from_user.id).split(". ")
			if int(message.text) >= 1 and int(message.text) <= (len(s) - 1):
				b = await message.reply("`Obtendo informações da disciplina...`")
				
				username, password = get_login(message.from_user.id)
				_, disc, disciplinas = discs(message.from_user.id, _login(username, password))
				
				disciplina_escolhida = disciplinas[int(message.text) - 1]
				boletim = _notas(disciplina_escolhida, disc)
				await b.edit(boletim)
			else:
				await message.reply("`Selecione um número correto.`")
			#else:
				#remove_wait(message.from_user.id)

