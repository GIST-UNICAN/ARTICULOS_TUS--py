# -*- coding: utf-8 -*-
"""
Created on Thu May 31 10:39:52 2018

@author: Andres
"""
from bs4 import BeautifulSoup
import urllib.request
import re
import csv
import pandas as pd

paginas = range(1, 6)
base_url = 'http://www.eldiariomontanes.es/temas/entidades/metrotus.html?pag={}'
tag_fecha = 'voc-date'
tag_titulo = 'voc-title'
tag_autor = 'voc-author-2'
regex_fecha = '^[0-9]*-.[0-9]*-.[0-9]*'
regex_fecha_compilada = re.compile(regex_fecha)
lista = list()
for pagina in paginas:
    content = urllib.request.urlopen(base_url.format(pagina)).read()
    soup = BeautifulSoup(content, "lxml")
    for articulo in soup.findAll('article'):
        try:
            fecha = regex_fecha_compilada.match(
                articulo.find('div').find('time').getText()).group(0)
            titulo = articulo.find('div').find('a')['title']
            autor = articulo.find('div').find('author').find('span').getText()
            lista.append((fecha, titulo, autor))
        except BaseException:
            pass
df = pd.DataFrame(lista, columns=['fecha', 'titular', 'autor'])
df['fecha'] = pd.to_datetime(df['fecha'])
df.to_excel('diario_montañes.xls')

# with open('diario_montañes.csv','w') as file:
#    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#    wr.writerow(lista)
