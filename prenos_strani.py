import requests 
import os

####################################################
#Prenos spletne strani
####################################################

#Najprej bom poimenoval url strani, iz katere zajemamo podatke, in datoteko, v katero bom shranil html. 
#Ker je oglasov za stanovanja 19 strani, bom najprej naredil seznam url povezav. 

seznam_url = []
for n in range(1,20):
    seznam_url.append(f'https://www.bolha.com/oddaja-stanovanja?page={n}')

stanovanja_imenik = "stanovanja"

#Sedaj bom definiral dve pomožni funkciji, s katerima si bom potem pomagal pri prenosu podatkov iz spletne strani. 

def prenesi_url_v_niz(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f"Napaka pri povezovanju do:{url}")
        return None
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print(f"Napaka pri prenosu strani:{url}")
        return None

def shrani_niz_v_datoteko(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

#Sedaj bom shrnanil spletno stran (spletne strani) v isto mapo, kjer se nahajam sedaj, v datoteko z imenom "stanovanja". 

#Najprej bom definiral funkcijo, ki bo to izvedla, potem pa bom to funkcijo preprosto pognal. 

def shrani_spletno_stran(directory, filename):
    text = ""
    for url in seznam_url:
        text += prenesi_url_v_niz(url)
    shrani_niz_v_datoteko(text, directory, filename)
    return None 

#Sedaj bom to funkcijo pognal in opravilo, ki smo ga želili izvesti v tej datoteki, bo zaključeno.

shrani_spletno_stran("podatki", stanovanja_imenik)
