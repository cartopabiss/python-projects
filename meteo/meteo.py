import json
import requests
import datetime
from prettytable import PrettyTable


def main():
    print("\n-------------------------------------METEO-------------------------------------------\n")
    
    hours = str(datetime.datetime.now().strftime("%H"))+"{}".format(":00")
    giorno = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    
    citta = ""
    while citta == "":
        try:
            citta = input("inserisci la località: ")
            citta = parse(citta)
            lat_lng = find_cordinate(citta)
        except:
            print("! ERROR........", "data not found")
            citta = ""
            continue

    URL = crea_url(lat_lng)
    risp = requests.get(URL).json()
    path = "projects\mateo\data\\risp_api.json"
    salva_risp_in_file(path, risp)
    print("dati aggiornati alle",hours, "del", split_data(giorno))
    tabella = accedi_ai_dati(path, giorno, hours)
    print(tabella)
   
    
    
def find_cordinate(nome):
    with open('projects\mateo\data\lat_lot.json', 'r') as file_dati:
        
        trovato = False
        dati = json.load(file_dati)
        for city in dati:
            
            if city["comune"] == nome:
                lat = city["lat"]
                lng = city["lng"]
                trovato = True
                print("città trovata")
                break
            
        if trovato != True:
            raise Exception("data not found")
        
    stringa_ris = lat+","+lng
    return stringa_ris




def crea_url(lat_lng):
    temp = lat_lng.split(",")
    lat = temp[0]
    lng = temp[1]
    url = "https://api.open-meteo.com/v1/meteofrance?latitude={latit}&longitude={lngt}&hourly=temperature_2m,precipitation&daily=temperature_2m_max,temperature_2m_min&timezone=auto".format(latit = lat, lngt = lng)
    return url



def salva_risp_in_file(path_f, risp):
    with open(path_f, 'w') as fj:
        json.dump(risp, fj, indent = 3)
     
        

def parse(stringa):
    stringa = stringa.strip().capitalize()
    return stringa

     
     
def accedi_ai_dati(path_f, day, hour):
    with open(path_f, 'r') as f:
        lista = json.load(f)
    
    tab = PrettyTable()
    tab.field_names = ["data", "ora", "temperatura", "precipitazioni(mm)", "temp. max.", "temp. min."]
    
    i = 0
    j = 0
    data_cop = ""
    for elem in lista["hourly"]["time"]:
        
        dat_or = elem.split("T")
        data = dat_or[0]
        data = split_data(data)
        ora = dat_or[1]
        temp = lista["hourly"]["temperature_2m"][i]
        prec = lista["hourly"]["precipitation"][i]
        
        if data == split_data(day) and ora == hour:
            tab.add_row(["===========", "======", "============", "==================", "===========", "==========="])
            tab.add_row([data_cop, ora, temp, prec, massima, minima])
            tab.add_row(["===========", "======", "============", "==================", "===========", "==========="])
        
        if prec > 0:
            prec = str(prec)+"  (pioggia)"
        
        i += 1
        if data != data_cop:
            data_cop = data
            tab.add_row(["-----------", "------", "------------", "------------------", "-----------", "-----------"])
            massima = lista["daily"]["temperature_2m_max"][j]
            minima = lista["daily"]["temperature_2m_min"][j]
            tab.add_row([data_cop, ora, temp, prec, massima, minima])
            
            j += 1
        else:
            tab.add_row(["**", ora, temp, prec, "**", "**"])
            
    return tab



def split_data(data):
    l = data.split("-")
    anno = l[0]
    mese = l[1]
    giorno = l[2]
    return "{g}-{m}-{a}".format(g = giorno, m = mese , a = anno)
    
    
    
if __name__ == '__main__':
    main()