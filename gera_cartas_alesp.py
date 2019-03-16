# -*- coding: future_fstrings -*-
from xml.dom import minidom
import xpath
import os
import json
import base64
import mimetypes


with open("templates/card_template_new.svg", 'r') as f:
  _carta = minidom.parse(f)

with open("autores-small.json", 'r', encoding='utf-8') as f:
  deputados = json.load(f)

with open("dados/partidos.json", 'r', encoding='utf-8') as f:
    _partidos = json.load(f)
    partidos = dict(map(lambda p: (p["sigla"], p["img"]), _partidos))


# abre imagem como base64
def openBase64(filename):
  with open(filename, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    mime, encoding = mimetypes.guess_type(filename)
    return f'data:{mime};base64,{encoded_string}'

for matricula, deputado in deputados.items():
  # começa com carta mestre
  carta = _carta.cloneNode(True)

  # troca nome
  elem_nome = xpath.find("//*[@id='texto_nome']/tspan/text()",carta)[0]
  elem_nome.nodeValue = deputado["nome"]

  # troca partido
  elem_partido = xpath.find("//*[@id='image_partido']", carta)[0]
  elem_partido.removeAttribute("sodipodi:absref")
  elem_partido.setAttribute("xlink:href", openBase64(partidos[deputado["partido"]]))

  # troca foto
  elem_foto = xpath.find("//*[@id='image_foto']", carta)[0]
  elem_foto.removeAttribute("sodipodi:absref")
  elem_foto.setAttribute("xlink:href", openBase64(deputado["local_img"]))

  elem_base = xpath.find("//*[@id='texto_base']/tspan/text()",carta)[0]
  elem_base.nodeValue = deputado["base"]


  with open(f'cartas/{deputado["nome"]}.svg', 'w', encoding='utf-8') as f:
    carta.writexml(f)
