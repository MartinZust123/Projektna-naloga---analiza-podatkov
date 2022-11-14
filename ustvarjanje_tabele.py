import re
import os
import csv

#############################################################
#V prvem bloku bomo ustvarili seznam oglasov. 
#############################################################

def preberi_datoteko_v_niz(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

#Sedaj si podatke shranimo v niz z imenom 'tekst'. 
tekst = preberi_datoteko_v_niz("podatki", "stanovanja1")

#Definirajmo funkcijo, ki html s oglasi spremeni v seznam oglasov. 
def stran_v_oglase(page_content):
    rx = re.compile(r'<article class="entity-body cf">'
                    r'(.*?)</article>',
                    re.DOTALL)
    ads = re.findall(rx, page_content)
    return ads

#Shranimo oglase v seznam oglasov
oglasi = stran_v_oglase(tekst)

#Definiramo funkcijo cena, ki bo nekakšen indikator, če je element seznam oglasi res oglas za stanovanje.
def cena(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatek o ceni."""
    rx = re.compile(r'<strong class="price price--hrk">(\W|\n)*?(?P<price>(\w|\.)*?)(&nbsp;<span class="currency">€)?[^0-9]*?</strong>',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = {}
    if data is not None:
        ad_dict["price"] = data.group("price")
    else:
        ad_dict["price"] = "Unknown"
    return ad_dict

#Sestavimo seznam cen oglasov, ki vsebuje slovarje. V nekaterih slovarjih je cena tudi neznana. Tiste ogalse želimo odstraniti iz seznama oglasov, saj 
#ne gre za oglase stanovanj, vendar jih je bilo težko izločiti z vzorcem.  
sez = []
oglasi = stran_v_oglase(tekst)
for ad in oglasi:
    ad_dict = cena(ad)
    sez.append(ad_dict)

odstrani_sez = []
odstrani_oglasi = []
for n in range(len(oglasi)):
    if sez[n]["price"] == "Unknown":
        odstrani_sez.append(sez[n])
        odstrani_oglasi.append(oglasi[n])

for e in odstrani_oglasi:
    oglasi.remove(e)

for e in odstrani_sez:
    sez.remove(e)

#Sedaj imamo v seznamu "oglasi" shrnajene le še prave oglase za stanovanja. 

################################################################################################################
#Naš naslednji cilj je iz seznama ogalsov izluščiti seznam, ki vsebuje slovar lastnosti za vsak oglas iz seznama
################################################################################################################

def parametri_poleg_cene(block):
    rxl = re.compile(r'<span class="entity-description-itemCaption">Lokacija: </span>(?P<location>.*?)<br />',
                    re.DOTALL)
    datal = re.search(rxl, block)
    ad_dict = {}
    ad_dict["location"] = datal.group("location")

    rxv = re.compile(r'Bivalna površina: (?P<size>.*?) m2',
    re.DOTALL)
    datav = re.search(rxv, block)
    if datav is not None:
        ad_dict["size"] = datav.group("size")
    else:
        ad_dict["size"] = "Unknown"

    rxd = re.compile(r'<time class="date date--full" datetime=.*? pubdate="pubdate">(?P<date>.*?)\.</time>')
    datad = re.search(rxd, block)
    ad_dict["date"] = datad.group("date")

    return ad_dict
    

#v seznam dodamo podatke o lokacijah.
for i in range(len(oglasi)):
    ad_dict = parametri_poleg_cene(oglasi[i])
    sez[i].update(ad_dict)


#################################################################
#V naslednjem koraku bomo ustvarili csv datoteko. 
#################################################################

def napisi_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def napisi_oglase_v_csv(ads, directory, filename):
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    napisi_csv(ads[0].keys(), ads, directory, filename)

napisi_oglase_v_csv(sez, "podatki", "stanovanja_Bolha.csv")