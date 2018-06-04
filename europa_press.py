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
paginas=range(1,150)
base_url='http://www.europapress.es/cantabria/{}/'

regex_fecha='(?P<letras>[a-z A-Z]*)(?P<fecha>[0-9]*/[0-9]*/[0-9]*)'
regex_fecha_compilada=re.compile(regex_fecha)
lista=list()
sesion= requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}
sesion.headers= headers
for pagina in paginas:
    web=base_url.format(pagina)
    content = sesion.get(web)
    soup = BeautifulSoup(content.text, "lxml")
    for articulo in soup.findAll('div',{'class':'articulo-info-texto'}):
#        print(articulo)
        try:
            url_articulo=articulo.find('h2').find('a', href=True)['href']
            titulo=articulo.find('h2').find('a').getText()
            cuerpo=articulo.find('div',{'class': 'articulo-primer-parrafo'}).getText()
            if re.search('metrotus', titulo+cuerpo, re.IGNORECASE) or re.search('metro-tus', titulo+cuerpo, re.IGNORECASE):
                content_article=sesion.get(url_articulo)
                soup_article = BeautifulSoup(content_article.text, "lxml")
                fecha= soup_article.find('div',{'class':'FechaPublicacionNoticia' }).getText()
                fecha=regex_fecha_compilada.match(fecha).group('fecha')
                fecha=datetime.strptime(fecha, '%d/%m/%Y')
                print(fecha)
                lista.append((fecha,titulo))
            
            autor=articulo.find('p',{'class': 'art_autor'}).find('a').getText()
            lista.append((fecha,titulo,autor))
        except AttributeError:
            pass
        except Exception as e:
            traceback.print_exc()
            
            pass
df = pd.DataFrame(lista, columns=['fecha','titular'])
df['fecha']=pd.to_datetime(df['fecha'])
df.to_excel('europa_press.xls')

#with open('diario_montañes.csv','w') as file:
#    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#    wr.writerow(lista)
        