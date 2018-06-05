# -*- coding: utf-8 -*-
"""
Created on Thu May 31 10:39:52 2018

@author: Andres
"""
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import csv
import pandas as pd
from datetime import datetime
import locale
import traceback
paginas = range(1, 2)
base_url = 'https://www.eldiario.es/temas/metro-tus/'

regex_fecha = '^[0-9]*-[0-9]*-[0-9]*'
regex_fecha_compilada = re.compile(regex_fecha)
lista = list()

for pagina in paginas:
    content = requests.get(base_url)
    soup = BeautifulSoup(content.text, "lxml")
    for articulo in soup.findAll('div', {'class': "mtflow"}):
        #        print(articulo)
        try:
            fecha = articulo.find(
                'p', {
                    'class': 'bkn dateline'}).find(
                'span', {
                    'class': 'date'}).getText()
#            fecha=datetime.strptime(fecha,'%d/%m/%Y')
#            print(fecha)
            titulo = articulo.find(
                'h2', {'class': 'bkn headline typ-x4'}).find('a')['title']
            print(titulo)
            autor = articulo.find(
                'p', {'class': 'bkn dateline'}).find('a')['title']
#            print(autor)
            lista.append((fecha, titulo, autor))
        except Exception as e:
            #            traceback.print_exc()

            pass
df = pd.DataFrame(lista, columns=['fecha', 'titular', 'autor'])
df['fecha'] = pd.to_datetime(df['fecha'])
df.to_excel('eldiarioes.xls')

# with open('diario_montañes.csv','w') as file:
#    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#    wr.writerow(lista)
