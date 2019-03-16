# -*- coding: future_fstrings -*-
from xml.dom import minidom
import xpath
import os

import base64
import mimetypes

class TemplateSVG:
    def __init__(self, templateFile):
        with open(templateFile, 'r') as arquivo:
            self.template = minidom.parse(arquivo)
            self.svg = self.template.cloneNode(True)

    def openBase64(self, filename):
        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            mime, encoding = mimetypes.guess_type(filename)
            return f"data:{mime};base64,{encoded_string}"

    def replaceImage(self, image_id, filename):
        _elem = xpath.find(f"//*[@id='{image_id}']", self.svg)[0]
        _elem.removeAttribute("sodipodi:absref")
        _elem.setAttribute("xlink:href", self.openBase64(filename))

    def replaceText(self, text_id, newtext):
        _elem = xpath.find(f"//*[@id='{text_id}']/tspan/text()",self.svg)[0]
        _elem.nodeValue = newtext

    def save(self, filepath):
        with open(f"{filepath}", "w", encoding="utf-8") as f:
            self.svg.writexml(f)
