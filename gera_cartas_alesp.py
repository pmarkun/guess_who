# -*- coding: future_fstrings -*-
import json
from gerador import TemplateSVG

with open("autores-small.json", 'r', encoding='utf-8') as f:
    deputados = json.load(f)

for matricula, deputado in deputados.items():
    # começa com carta mestre
    carta = TemplateSVG("templates/card_template_new.svg")

    carta.replaceImage("image_partido", deputado["partido_img"])

    carta.replaceImage("image_foto", deputado["local_img"])

    carta.replaceText("texto_nome", deputado["nome"])

    carta.replaceText("texto_base", deputado["base"])

    carta.save(f"output/cartas/{deputado['nome']}.svg")
