from IPython.display import Image
from IPython.core.display import HTML
import os
import csv
from termcolor import colored, cprint


Image(url= "weather.png")


import datetime
import json
import urllib.request
import pandas as pd
import json
import pandas as pd
from pandas.io.json import json_normalize 



def url_builder(city_id,city_name,country):
    user_api = 'bfa11916159cf7b15490b701de14db1b' 
    unit = 'metric' 
    if(city_name!=""):
        api = 'http://api.openweathermap.org/data/2.5/weather?q='
        full_api_url = api + str(city_name) +','+ str(country)+ '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id='
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    
    return full_api_url


def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
    city=raw_api_dict.get('name'),
    country=raw_api_dict.get('sys').get('country'),
    temp_max=raw_api_dict.get('main').get('temp_max'),
    temp_min=raw_api_dict.get('main').get('temp_min'),
    )
    return data



def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('')
    print('Température à : {}, {}:'.format(data['city'], data['country']))
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('---------------------------------------')



def WriteCSV(data):
    with open('weatherOpenMap.csv', 'a') as t: 
        w = csv.DictWriter(t, data.keys())
        w.writeheader()
        w.writerow(data)

def ReadCSV():
    try:
        with open("weatherOpenMap.csv",'r') as f:
            csv_contenu = csv.reader(f,delimiter=",")
            reader = csv.DictReader(f)
            dic={}
        for row in reader:
            print (row['city'])
            dic.update(row)
            f.close()
        return dic
    except IOError:
        print("Fichier n'est pas trouvé")

def getVilles():
    with open('city.list.json') as t:
        d = json.load(t)
        villes=pd.DataFrame(d)
    return villes

villes = getVilles()
villesFr = villes[villes["country"]=='FR']['id']

import time

if __name__ == '__main__':
    try:
        city_name=''
        country='FR'
        compteur = 0
        
        for ville_id in villesFr :
            city_id= ville_id
            print(colored('Generation de l url ', 'red',attrs=['bold']))
            url=url_builder(city_id,city_name,country)
            print(colored('Invocation du API afin de recuperer les données', 'red',attrs=['bold']))
            data=data_fetch(url)
            print(colored('Formatage des donnée', 'red',attrs=['bold']))
            data_orgnized=data_organizer(data)
            print(colored('Affichage de données ', 'red',attrs=['bold']))
            data_output(data_orgnized)
            print(colored('Enregistrement des données à dans un fichier CSV ', 'green',attrs=['bold']))
            WriteCSV(data_orgnized)
            time.sleep(0.2)
            print(colored('Lecture des données à partir un fichier CSV ', 'green',attrs=['bold']))
        compteur += 1
            
    except IOError:
        print('no internet')
