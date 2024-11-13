import requests
from bs4 import BeautifulSoup as bs

from functools import partial, wraps
from pyrogram import filters

from plugins.sql.sql import *

cmd = partial(filters.command, prefixes=list("/"))

def _login(username, senha):
	with requests.Session() as session:
		login = "https://suap.ifma.edu.br/accounts/login/?next=/"
		headers = {"referer": login}
		
		login_page = session.get(login, headers=headers)
		login_html = bs(login_page.text, 'html.parser')
		
		csrf = login_html.find('input', {"type": "hidden"})["value"]
		
		payload = {"csrfmiddlewaretoken": csrf, "username": username, "password": senha}
		
		boletim = f"https://suap.ifma.edu.br/edu/aluno/{username}/?tab=boletim"
		
		s = session.post(login, data=payload, headers=headers)
		response = session.get(boletim, headers=headers)
		
		if "login" not in s.url:
			return response.text
		else:
			return None
	

def discs(id, response):
    disciplinas = []
    sorted_disciplina = ""
    soup = bs(response, "html.parser")
    disc = soup.find_all("td", {"headers": "th_disciplina"})
    for i in disc:
        k = i.text.split("-")[1]
        disciplinas.append(k)
    for index, disciplina in enumerate(disciplinas, start=1):
        sorted_disciplina += f"{index}. {disciplina.strip()}\n"
    if not get_disc(str(id)):
        add_disc(str(id), sorted_disciplina)
    else:
        return sorted_disciplina, disc, disciplinas
	   	
	   
def _notas(disciplina_escolhida, disciplinas):
    for nota in disciplinas:
        for i in nota:
            if disciplina_escolhida in i:
                status = nota.parent.find("td", {"headers": "th_situacao"}).text
                total_aulas = nota.parent.find("td", {"headers": "th_total_aulas"}).text
                aulas_dadas = nota.parent.find("td", {"headers": "th_ch"}).text
                faltas = nota.parent.find("td", {"headers": "th_total_faltas"}).text
                f1 = nota.parent.find("td", {"headers": "th_n1f"}).text
                f2 = nota.parent.find("td", {"headers": "th_n2f"}).text
                f3 = nota.parent.find("td", {"headers": "th_n3f"}).text if nota.parent.find("td", {"headers": "th_n3f"}) else None
                f4 = nota.parent.find("td", {"headers": "th_n4f"}).text if nota.parent.find("td", {"headers": "th_n3f"}) else None
                freq = nota.parent.find("td", {"headers": "th_frequencia"}).text
                md = nota.parent.find("td", {"headers": "th_mfd"}).text
                if nota.parent.find("td", {"headers": "th_n1n"}):
                    if nota.parent.find("td", {"headers": "th_nr1"}):
                        if nota.parent.find("td", {"headers": "th_nr1"}).text:
                            if float((nota.parent.find("td", {"headers": "th_nr1"}).text).replace(",", ".")) > float((nota.parent.find("td", {"headers": "th_n1n"}).text).replace(",", ".")):
                                n1 = nota.parent.find("td", {"headers": "th_nr1"}).text
                            else:
                                if nota.parent.find("td", {"headers": "th_n1n"}).text == "-":
                                    n1 = "nota não lançada"
                                else:
                                    n1 = nota.parent.find("td", {"headers": "th_n1n"}).text
                        else:
                            if nota.parent.find("td", {"headers": "th_n1n"}).text == "-":
                                n1 = "nota não lançada"
                            else:
                                n1 = nota.parent.find("td", {"headers": "th_n1n"}).text
                else:
                    n1 = None
                    
                if nota.parent.find("td", {"headers": "th_n2n"}):
                    if nota.parent.find("td", {"headers": "th_nr2"}):
                        if nota.parent.find("td", {"headers": "th_nr2"}).text:
                            if float((nota.parent.find("td", {"headers": "th_nr2"}).text).replace(",", ".")) > float((nota.parent.find("td", {"headers": "th_n2n"}).text).replace(",", ".")):
                                n2 = nota.parent.find("td", {"headers": "th_nr2"}).text
                            else:
                                if nota.parent.find("td", {"headers": "th_n2n"}).text == "-":
                                    n2 = "nota não lançada"
                                else:
                                    n2 = nota.parent.find("td", {"headers": "th_n2n"}).text
                        else:
                            if nota.parent.find("td", {"headers": "th_n2n"}).text == "-":
                                n2 = "nota não lançada"
                            else:
                                n2 = nota.parent.find("td", {"headers": "th_n2n"}).text
                    else:
                        if nota.parent.find("td", {"headers": "th_n2n"}).text == "-":
                            n2 = "nota não lançada"
                        else:
                            n2 = nota.parent.find("td", {"headers": "th_n2n"}).text
                else:
                    n2 = None
                    
                if nota.parent.find("td", {"headers": "th_n3n"}):
                    if nota.parent.find("td", {"headers": "th_nr3"}):
                        if nota.parent.find("td", {"headers": "th_nr3"}).text:
                            if float((nota.parent.find("td", {"headers": "th_nr3"}).text).replace(",", ".")) > float((nota.parent.find("td", {"headers": "th_n3n"}).text).replace(",", ".")):
                                n3 = nota.parent.find("td", {"headers": "th_nr3"}).text
                            else:
                                if nota.parent.find("td", {"headers": "th_n3n"}).text == "-":
                                    n3 = "nota não lançada"
                                else:
                                    n3 = nota.parent.find("td", {"headers": "th_n3n"}).text
                        else:
                            if nota.parent.find("td", {"headers": "th_n3n"}).text == "-":
                                n3 = "nota não lançada"
                            else:
                                n3 = nota.parent.find("td", {"headers": "th_n3n"}).text
                else:
                    n3 = None
                    
                if nota.parent.find("td", {"headers": "th_n4n"}):
                    if nota.parent.find("td", {"headers": "th_n4n"}).text == "-":
                        n4 = "nota não lançada"
                    else:
                        n4 = nota.parent.find("td", {"headers": "th_n4n"}).text
                else:
                    n4 = None
                    
                if n3 == None and n4 == None:
                    if n2 == "nota não lançada":
                        n2 = 0
                        n1.replace(",", ".")
                        an = (float(n1) + n2)
                        ps = 28 - an
                        approved = "Você já foi aprovado na disciplina" if an >= 14 else f"Faltam {ps} pontos para você ser aprovado!"
                    boletim = f"""
`Disciplina: {disciplina_escolhida.strip()}
	   			
Situação: {status}
Total de aulas: {total_aulas}
Aulas dadas: {aulas_dadas}
Frequência: {freq}
Faltas: {faltas}
	   			
1° bimestre
Nota: {n1}
Faltas: {f1}
	   			
2° bimestre
Nota: {n2}
Faltas: {f2}

Média final: {md}
{approved}`"""
                else:
                    if n4 == "nota não lançada":
                        n4 = 0
                        for i in [n1, n2, n3]:
                            i.replace(",", ".")
                        an = (float(n1) + float(n2) + float(n3) + n4)
                        ps = 28 - an
                        approved = "Você já foi aprovado na disciplina" if an >= 28 else f"Faltam {ps} pontos para você ser aprovado!"
                    boletim = f"""
`Disciplina: {disciplina_escolhida.strip()}
	   			
Situação: {status}
Total de aulas: {total_aulas}
Aulas dadas: {aulas_dadas}
Frequência: {freq}
Faltas: {faltas}
	   			
1° bimestre
Nota: {n1}
Faltas: {f1}
	   			
2° bimestre
Nota:  {n2}
Faltas: {f2}
	   			
3° bimestre
Nota: {n3}
Faltas: {f3}
	   			
4° bimestre
Nota: {n4}
Faltas: {f4}

Média final: {md}
{approved}`"""
                    
                return boletim
	   			
