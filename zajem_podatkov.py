import requests
import re
import os
import csv

######################################################################################
#Najprej definiramo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
######################################################################################

#definiramo URL glavne strani Bolhe za oglase s stanovanji
stanovanja_url = 'https://www.bolha.com/oddaja-stanovanja'
#mapa, v katero bomo shranili podatke
stanovanja_imenik = 'stanovanja'
#ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'index_stanovanja.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'stanovanja.csv'

def prenesi_url_v_niz(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Napaka pri povezovanju do:", url)
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        print("Napaka pri prenosu strani:", url)
        return None

def shrani_niz_v_datoteko(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    text = prenesi_url_v_niz(stanovanja_url)
    shrani_niz_v_datoteko(text, directory, filename)
    return None 

#############################################################
#Po pridobitvi podatkov jih želimo obdelati.
#############################################################

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

save_frontpage("Projekt","stanovanja")
tekst = read_file_to_string("Projekt", "stanovanja")

def page_to_ads(page_content):
    rx = re.compile(r'<article class="entity-body cf">'
                    r'(.*?)</article>',
                    re.DOTALL)
    ads = re.findall(rx, tekst)
    return ads

def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu,
    lokaciji, datumu objave in ceni ter vrne slovar, ki vsebuje ustrezne
    podatke"""
    rx = re.compile(r'<h3.*>(?P<name>.*?)</a></h3>'
                    r'.*?"pubdate">(?P<time>.*?)</time>'
                    r'.*?<strong class="price price--hrk">\s*(?P<price>.*?)(&|\s</strong>)',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()

    # Ker nimajo vsi oglasi podatka o lokaciji, to rešimo z dodatnim vzorcem
    rloc = re.compile(r'Lokacija: </span>(?P<location>.*?)<br />')
    locdata = re.search(rloc, block)
    if locdata is not None:
        ad_dict['location'] = locdata.group('location')
    else:
        ad_dict['location'] = 'Unknown'

    return ad_dict

print(get_dict_from_ad_block(page_to_ads(tekst)[0]))