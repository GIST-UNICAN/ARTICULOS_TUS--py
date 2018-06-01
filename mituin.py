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
paginas=range(1,10)
extraer_dic={1: tuple(range (1,31)), 2:tuple(range(1,28)), 3:tuple(range(1,31)), 4:tuple(range(1,30)), 5:tuple(range(1,31))}
base_url='https://www.mituin.com/tema/metro-tus/pag-{}'

regex_fecha='^[0-9]*-[0-9]*-[0-9]*'
regex_fecha_compilada=re.compile(regex_fecha)
lista=list()

for pagina in paginas:
    web=base_url.format(pagina)
    content = requests.get(web)
    soup = BeautifulSoup(content.text, "lxml")
    for articulo in soup.findAll('div',{'class': "col-xs-9"}):
#        print(articulo)
        try:
            fecha=articulo.find('p',{'class':'art_meta'}).getText()
            fecha=datetime.strptime(regex_fecha_compilada.match(fecha).group(0),'%d-%m-%Y')
            titulo=articulo.find('h2').find('a').getText()
            autor=articulo.find('p',{'class': 'art_autor'}).find('a').getText()
            lista.append((fecha,titulo,autor))
        except Exception as e:
            traceback.print_exc()
            
            pass
df = pd.DataFrame(lista, columns=['fecha','titular','autor'])
df['fecha']=pd.to_datetime(df['fecha'])
df.to_excel('mituin.xls')

#with open('diario_montañes.csv','w') as file:
#    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#    wr.writerow(lista)
        