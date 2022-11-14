import re
import os

#############################################################
#Po pridobitvi podatkov jih želimo obdelati.
#############################################################

def preberi_datoteko_v_niz(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

#sedaj si podatke shranimo v niz z imenom 'tekst'. 
tekst = preberi_datoteko_v_niz("podatki", "stanovanja1")

#definirajmo funkcijo, ki html s oglasi spremeni v seznam oglasov. 
def stran_v_oglase(page_content):
    rx = re.compile(r'<article class="entity-body cf">'
                    r'(.*?)</article>',
                    re.DOTALL)
    ads = re.findall(rx, page_content)
    return ads

oglasi = stran_v_oglase(tekst)

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

print(sez)