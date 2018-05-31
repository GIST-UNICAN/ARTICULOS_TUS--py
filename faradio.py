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
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
paginas=range(1,7)
base_url='http://www.elfaradio.com/tag/metrotus/page/{}/'
tag_fecha='voc-date'
tag_titulo='voc-title'
tag_autor='voc-author-2'
regex_fecha='[0-9]*.*[0-9]'
regex_fecha_compilada=re.compile(regex_fecha)
lista=list()
for pagina in paginas:
    content = urllib.request.urlopen(base_url.format(pagina)).read()
    soup = BeautifulSoup(content, "lxml")
    for articulo in soup.findAll('div',{'class': "articleinner"}):
        try:
            fecha=regex_fecha_compilada.match(articulo.find('span').getText().strip()).group(0)
            fecha=datetime.strptime(fecha,'%d  de %B de %Y')
            titulo=articulo.find('h2').find('a')['title'][18:]
            autor=articulo.find('span').find('a').getText()
            lista.append((fecha,titulo,autor))
        except Exception as e:
            print(e)
            pass
df = pd.DataFrame(lista, columns=['fecha','titular','autor'])
df['fecha']=pd.to_datetime(df['fecha'])
df.to_excel('faradio.xls')

#with open('diario_montañes.csv','w') as file:
#    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#    wr.writerow(lista)
        