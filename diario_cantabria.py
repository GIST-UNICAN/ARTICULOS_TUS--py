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
paginas=range(1,3)
extraer_dic={1: tuple(range (1,31)), 2:tuple(range(1,28)), 3:tuple(range(1,31)), 4:tuple(range(1,30)), 5:tuple(range(1,31))}
base_url='http://www.eldiariocantabria.es/archive/content/2018/{}/{}?page={}'

regex_fecha='[0-9]*.*[0-9]'
regex_fecha_compilada=re.compile(regex_fecha)
lista=list()
for mes, lista_dias in extraer_dic.items():
    for dia in lista_dias:
        print(mes,'-',dia)
        for pagina in paginas:
            web=base_url.format(mes,dia,pagina)
            print (web)
            content = requests.get('http://www.eldiariocantabria.es/archive/content/2018/2/02?page=1')
            soup = BeautifulSoup(content.text, "lxml")
            for articulo in soup.findAll('div',{'class': "article-data"}):
                try:
                    fecha=datetime(2018,mes,dia,0,0,0)
                    titulo=articulo.find('h3').find('a')['title']
                    if titulo!='La Unión de Consumidores pide restablecer las líneas anteriores al MetroTUS “por el bien de la ciudad”':
#                        print(fecha)
                        cuerpo=articulo.find('div',{'class': 'summary'}).getText()
                        print(titulo)
                        if re.search('metrotus', titulo+cuerpo, re.IGNORECASE) or re.search('metro-tus', titulo+cuerpo, re.IGNORECASE):
                            print(titulo)
                            lista.append((fecha,titulo))
                except Exception as e:
                    traceback.print_exc()
                    
                    pass
#df = pd.DataFrame(lista, columns=['fecha','titular','autor'])
#df['fecha']=pd.to_datetime(df['fecha'])
#df.to_excel('faradio.xls')

#with open('diario_montañes.csv','w') as file:
#    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#    wr.writerow(lista)
        