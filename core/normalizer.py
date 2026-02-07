import urllib.parse
import html
import unicodedata
import re

def normalize(text):
    if not text:
        return ""

    text = unicodedata.normalize("NFKC",text)

    text = urllib.parse.unquote(text)
    text = urllib.parse.unquote(text)

    text = text.replace("\x00","")

    text = text.lower()

    text = re.sub(r"\s+", " ", text)  

    return text   