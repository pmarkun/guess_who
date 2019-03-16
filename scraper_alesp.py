from lxml.html import parse
from urllib import request
from urllib.parse import quote
import os
import json

def savejson(data, path):
  with open(path, 'w', encoding='utf-8') as out:
    json.dump(data, out, ensure_ascii=False, indent=2, sort_keys=True)

def getParlamentares():
    url = "https://www.al.sp.gov.br/alesp/deputados-estaduais/"
    soup = parse(request.urlopen(url)).getroot()
    linhas = soup.cssselect(".tabela tbody tr")
    autores = {}
    for p in linhas:
        nome = p.xpath('.//td/a')[0].get('href').split("=")[1]
        autores[nome] = {}
        autores[nome]['nome'] = p.xpath('.//td/a')[0].text.strip()
        autores[nome]['area'] = p.xpath('.//td')[1].text.strip()
        autores[nome]['base'] = p.xpath('.//td')[2].text.strip()
        autores[nome]['partido'] = p.xpath('.//td')[3].text.strip()
        autores[nome]['url'] = "https://www.al.sp.gov.br" + p.xpath('.//td/a')[0].get('href')
        autores[nome]['matricula'] = autores[nome]['url'].split("=")[1]
        print("Getting "+ autores[nome]['nome'])

    return autores

def getFotos(autores):
    for matricula in autores:
        path = "data/deputados/"+matricula+".jpg"
        if not os.path.exists(path):
            soup = parse(request.urlopen(autores[matricula]['url'])).getroot()
            foto = soup.cssselect("#conteudo img.img-thumbnail")[0].getnext().get('href')
            request.urlretrieve(quote(foto, safe='/:?=&'), path)
        autores[matricula]["local_img"] = path
    return autores

def getPartidos(autores):
    with open("data/partidos.json", 'r', encoding='utf-8') as f:
        partidos = json.load(f)
        partidos = dict(map(lambda p: (p["sigla"], p["img"]), partidos))
        for matricula in autores:
            autores[matricula]["partido_img"] = "data/"+partidos[autores[matricula]["partido"]]
    return autores

autores = getParlamentares()
autores = getFotos(autores)
autores = getPartidos(autores)
savejson(autores, "data/deputados.json")
