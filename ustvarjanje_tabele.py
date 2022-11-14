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
tekst = preberi_datoteko_v_niz("podatki", "stanovanja")

#definirajmo funkcijo, ki html s oglasi spremeni v seznam oglasov. 
def stran_v_oglase(page_content):
    rx = re.compile(r'<article class="entity-body cf">'
                    r'(.*?)</article>',
                    re.DOTALL)
    ads = re.findall(rx, page_content)
    return ads

seznam = stran_v_oglase(tekst)
print(seznam[:10])

def pridobi_parametre_iz_oglasa(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o lokaciji,
    datumu objave, ceni, vrsti stanovanja in velikosti ter vrne slovar, ki vsebuje ustrezne
    podatke"""
    rx = re.compile(r'.*?<strong class="price price--hrk">\s*(?P<price>)&nbsp;<span class="currency">€</span>.?(</strong>)',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = {}
    if data is not None:
        ad_dict['price'] = data.group('price')
    else:
        ad_dict['price'] = 'Unknown'
    return ad_dict

sez = []
oglasi = stran_v_oglase(tekst)
for ad in oglasi[10]:
    ad_dict = pridobi_parametre_iz_oglasa(ad)
    sez.append(ad_dict)

print(sez)

def seznam(sez):
    sez.append(3)
    return sez