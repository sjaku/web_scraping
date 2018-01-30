# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib
import os
import re
import time
#import mysql_functions
import mysql_fun
import functions
import math
import unicodedata

# Variables definition #
csvfile_features = "products_features.csv"
csvfile_data = "products_data.csv"
destinationPath = "/Users/szymon/PycharmProjects/my_project/selgros/"


# Funkcja pomocnicza, zamienia chyba dziwne znaki #
def multiple_replace(string, rep_dict):
    pattern = re.compile("|".join([re.escape(k) for k in rep_dict.keys()]), re.M)
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)


url_klocki = "http://selgros24.pl/Dla-dzieci/Zabawki/Klocki-pc1121.html"
url_product = "http://selgros24.pl/Dla-dzieci/Zabawki/Klocki/Ninjago/KLOCKI-LEGO-NINJAGO-PUSTYNNA-BLYSKAWICA-70622-pp107044.html"
url_product2 = "http://selgros24.pl/Dla-dzieci/Zabawki/Klocki/LEGO-Ninjago/KLOCKI-LEGO-NINJAGO-SMOK-MISTRZA-WU-70734-pp83894.html"
url_product3 = "http://selgros24.pl/Dla-dzieci/Zabawki/Klocki/LEGO-Mindstorms/KLOCKI-LEGO-MINDSTORMS-EV3-31313-pp71042.html"


def extract_thumbnail_images(url):
    images_list = []
    start = time.time()
    print('[Start] - rozpoczeto przetwarzanie url:', url)
    count = 0

    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.content, "html.parser")

    #mysql_functions.delete_query()
    mysql_functions.truncate_query()

    for article in soup.findAll("article", class_="small-product"):
        #images = [img for img in article.findAll('img')]
        img = article.find('img', class_='packshot')
        alt = img.get('alt')
        filename = alt + '.jpg'
        src = img.get('src')
        src = removeNonAscii(src)

        idx_last_slash = src.rfind('/')
        filename = src[idx_last_slash + 1:]

        pathfile = os.path.join(destinationPath, "thumbnails")
        newPath = os.path.join(pathfile, filename)

        #print('src: ", src, "newPath: ", newPath

        images_list = [src, newPath]
        print (images_list)
        mysql_functions.insert_query(images_list)
        #urllib.urlretrieve(src, newPath)

        count = count + 1
        end = time.time()
    print('[End] - pobrano:', count, 'miniaturek do:', destinationPath, 'w czasie:', '%.2gs' % (end - start))
#extract_thumbnail_images(url_klocki)


#funkcja pobierajaca url zdjecia ze strony produktu
#zapisuje do /selgros/products_images
#oraz do katalogu sklepu /img/lego
def extract_product_images(item_url):
    source_code = requests.get(item_url)
    soup = BeautifulSoup(source_code.content, "html.parser")

    diskPath = "/Users/szymon/PycharmProjects/my_project/selgros/"
    localhostPath = "http://localhost:8585/prestashop/img/lego/"
    directory_images = "products_images"

    images_list = []

    for item in soup.find_all('div', class_='item'):

        img = item.find('img', class_='default')
        #usunicie znakow z nazwy pliku
        if img is not None:
            alt = img.get('alt')
            filename = alt+'.jpg'
            src = img.get('src').encode('utf-8')
            #src = src.replace(u'®', u'')
            #src = img.get('src').encode('utf-8')
            #src = src.replace('\xc2\xae', '')
            #™
            #src = src.replace('™', '')
            #src = removeNonAscii(src)
            print('src: ', src)


            # pobranie nazwy pliku ze zmiennej src po osatnim ukosniku
            idx_last_slash = src.rfind('/')
            filename = src[idx_last_slash+1:]
            filename = filename.replace('™', '')
            filename = filename.replace('®', '')
            filename = filename.replace('’', '')
            filename = filename.replace('—', '')
            print('filename: ', filename)
            # f = multiple_replace(filename_slash, {'%': '_'})

            disk_temp = os.path.join(diskPath, directory_images)
            #pathfile = multiple_replace(pathfile, {'/': '', '"': '', '%': '_'})
            #print('pathfile: ", localhost_temp
            url_disk = os.path.join(disk_temp, filename)
            print('url_disk: ', url_disk)

            localhost_temp = os.path.join(localhostPath, directory_images)
            url_localhost = os.path.join(localhost_temp, filename)

            #print('url_localhost: ", url_localhost

            urllib.urlretrieve(src, url_disk)
            #print alt, pathfile, local
            images=[url_disk, url_localhost]
            images_list.append(images)
            #print type(images_list)
            print (images_list)


            #mysql_fun.insert_images(images_list)
            #mysql_functions.insert_query(images_list)


#testowe uruchomienie powyzszej funkcji dla 1 produktu
#url_tm = "http://selgros24.pl/Dla-dzieci/Zabawki/Klocki/LEGO-Star-Wars/KLOCKI-LEGO-STAR-WARS-SIERZANT-JYN-ERSO-75119-pp102420.html"
#extract_product_images(url_tm)

#NIE WYKORZYSTYWANA OBECNIE
#zapisanie zdjec na dysku w folderze sklepu

def extract_product_images_soup(soup):
    images_list=[]
    XAMPPPath = "/Applications/XAMPP/xamppfiles/htdocs/sklep/img/lego/"
    global title

    for item_name in soup.find_all('div', attrs={'id': 'main-container'}):
        title = item_name.find('h1').text.encode("utf-8")
        # ™
        '''title = title.replace('™', '')
        # ®
        title = title.replace('®', '')
        # —
        title = title.replace('—', '')
        # ’
        title = title.replace('’', '')
        #print('title: " + title
        '''

    for item in soup.find_all('div', class_='item'):
        img = item.find('img', class_='default')
        if(img is not None):
            alt = img.get('alt')
            filename = alt+'.jpg'
            src = img.get('src').encode('utf-8')
            # ™
            #src = src.replace('™', '')
            #®
            #src = src.replace('®', '')
            #—
            #src = src.replace('—', '')
            #’
            #src = src.replace('’', '')


            #pobranie nazwy pliku ze zmiennej src po osatnim ukosniku
            idx_last_slash = src.rfind('/')
            filename = src[idx_last_slash+1:]
            print('filename: ', filename)
            #f = multiple_replace(filename_slash, {'%': '_'})
            filename = filename.replace('™', '')
            filename = filename.replace('®', '')
            filename = filename.replace('—', '')
            filename = filename.replace('’', '')
            print('src: ', src)
            print('filename: ', filename)

            pathfile = os.path.join(destinationPath, "images")
            #pathfile = multiple_replace(pathfile, {'/': '', '"': '', '%': '_'})
            print('pathfile: ', pathfile)

            newPath = os.path.join(pathfile, filename)
            print('newPath: ', newPath)
            newPathXampp = os.path.join(XAMPPPath, filename)

            #zapisanie zdjec w katalogu gdzie jest skrypt pythona
            #urllib.urlretrieve(src, newPath)
            #zapisanie zdjec w lokalizacji serwera XAMPP
            urllib.urlretrieve(src, newPathXampp)

            localPath = "http://localhost/sklep/img/lego/"
            livePath = "http://www.kreatywneklocki.pl/img/lego/"
            local_filename = os.path.join(localPath, filename)
            print('local_filename: ',  local_filename)
            live_filename = os.path.join(livePath, filename)
            print('live_filename: ', live_filename)

            images=[title, newPath, local_filename, live_filename]
            images_list.append(images)

            mysql_fun.insert_images(images_list)

            #print images_list
            #return local_filename

        else:
            pass


def get_max_category_pages(url_klocki):
    r = requests.get(url_klocki)
    soup = BeautifulSoup(r.content, "html.parser")

    toys_obj = soup.find_all("div", class_="itemsPagging", limit=1)
    t_list = []
    for row in toys_obj:
        for link in row.find_all('a'):
             t = link.text
             #print t, type(t)
             t_list.append(t)
             #print (t_list)

        max_id_3td_position_on_list = int(len(t_list)-1)
        #print (max_id_3td_position_on_list)
        max_id_max = int(max(t_list))
        #print (max_id_max)

        if max_id_3td_position_on_list == max_id_max:
            max_id = max_id_3td_position_on_list
        elif max_id_3td_position_on_list > max_id_max:
            max_id = max_id_3td_position_on_list+1
        elif max_id_3td_position_on_list < max_id_max:
            max_id = max_id_max

        #print('Founded:', max_id ,'pages')
        return max_id
#get_max_category_pages(url_klocki)


count = 11

def get_data_save_CSV(url):
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.content, "html.parser")
    global count, typ, kategoria, kolor, material, waga, poprzednia_cena_sprzedazy_brutto
    typ = ''
    kategoria = ''
    kolor = ''
    material = ''
    waga = ''

    extract_product_images_soup(soup)

    courses_list = []
    count += 1
    for item_name in soup.find_all('div', attrs={"id" :'main-container'}):
        title = item_name.find('h1').text.encode("utf-8")
        # ™
        '''title = title.replace('™', '')
        # ®
        title = title.replace('®', '')
        # —
        title = title.replace('—', '')
        # ’
        title = title.replace('’', '')
        print (title)
        #title = removeNonAscii(title)'''

        #poczatek stringu z kodem
        code_length = len(title)
        #koniec stringu z kodem
        code_last_space = title.rfind(' ')
        code = title[code_last_space+1:code_length]
        #print('kod: ',code)

        prodDesc_class = item_name.find('div', class_='productDesc')
        marka_source = prodDesc_class.find('p').text
        marka_source_strip = marka_source.strip()
        marka_idx = marka_source_strip.find(' ')
        marka = marka_source_strip[marka_idx + 1:]

        marka = marka.replace('Star Wars Constraction', 'Star Wars')
        marka = marka.replace('LEGO City Airport', 'LEGO City')
        marka = marka.replace('LEGO City Demolition', 'LEGO City')
        marka = marka.replace('LEGO City Great Vehicles', 'LEGO City')
        marka = marka.replace('LEGO City Police', 'LEGO City')
        marka = marka.replace('LEGO City Town', 'LEGO City')
        marka = marka.replace('LEGO City Volcano Explorers', 'LEGO City')
        marka = marka.replace('LEGO DUPLO Town', 'LEGO Duplo')
        marka = marka.replace('LEGO DUPLO Disney TM', 'LEGO Duplo')
        marka = marka.replace('LEGO DUPLO Doc McStuffins', 'LEGO Duplo')
        marka = marka.replace('LEGO DUPLO My First', 'LEGO Duplo')
        marka = marka.replace('LEGO DUPLO Super Heroes', 'LEGO Duplo')
        #marka = marka.replace('LEGO Juniors', 'LEGO Juniors')
        #marka = marka.replace('Juniors', 'LEGO Juniors')
        marka = marka.replace('Disney Princess', 'LEGO Disney')

        #print('Marka: ", marka
        #idx_last_slash = src.rfind('/')
        #filename = src[idx_last_slash + 1:]




        if ((item_name.find('div', class_='oldPrice')) is None):
            old_price = float()

        else:
            old_price = float(item_name.find('div', class_='oldPrice').text)
            print('Old price: ', old_price)


        price_netto = item_name.find('div', class_="netto").text
        # strip() jest potrzebny, zeby usunac znaki entera itp i zeby wyswietlalo pobrane dane w jednym wierszu
        #price_netto = price_netto.strip()
        netto_float = float(price_netto.split(" ")[0])
        price_brutto = item_name.find('div', class_='actualPrice').text
        brutto_float = float(price_brutto.split(" ")[0])
        round_brutto_price = round(brutto_float, 1)

        marza_do_100 = 0.12
        marza_100_200 = 0.10
        marza_200_300 = 0.08
        marza_300_400 = 0.06
        marza_od_400 = 0.05
        VAT = 0.23

        if brutto_float < 100.00:
            cena_sprzedazy_brutto = round((netto_float * VAT) + netto_float + (netto_float * marza_do_100), 1)
            if old_price !=0:
                poprzednia_cena_sprzedazy_brutto = round( old_price + (old_price * marza_do_100), 1)
        elif brutto_float >= 400.00:
            cena_sprzedazy_brutto = round((netto_float * VAT) + netto_float + (netto_float * marza_od_400), 1)
            if old_price != 0:
                poprzednia_cena_sprzedazy_brutto = round(old_price + (old_price * marza_od_400), 1)
        elif brutto_float >= 300.00:
            cena_sprzedazy_brutto = round((netto_float * VAT) + netto_float + (netto_float * marza_300_400), 1)
            if old_price != 0:
                poprzednia_cena_sprzedazy_brutto = round(old_price + (old_price * marza_300_400), 1)
        elif brutto_float >= 200.00:
            cena_sprzedazy_brutto = round((netto_float * VAT) + netto_float + (netto_float * marza_200_300), 1)
            if old_price != 0:
                poprzednia_cena_sprzedazy_brutto = round(old_price + (old_price * marza_200_300), 1)
        elif brutto_float >= 100.00:
            cena_sprzedazy_brutto = round((netto_float * VAT) + netto_float + (netto_float * marza_100_200), 1)
            if old_price != 0:
                poprzednia_cena_sprzedazy_brutto = round(old_price + (old_price * marza_100_200), 1)

        print('brutto selgros: ', round_brutto_price)
        cena_sprzedazy_brutto = math.ceil(cena_sprzedazy_brutto)
        print('brutto sklep KK: ', math.ceil(cena_sprzedazy_brutto))


        short_desc = item_name.find('div', class_='short').text.encode("utf-8")
        short_desc = short_desc.replace(';', ',')
        #short_desc = removeNonAscii(short_desc)
        #print short_desc
        params = item_name.find('div', class_='short long')

        # Obliczenie kwoty brutto sprzedazy produktu obnizonego:
        # (Kwota brutto (po obnizce) na stronie selgros + moja marża) - obniżka % jaką daje selgros

        if old_price != 0:
            discount = str(int(100 - round((round_brutto_price / old_price) * 100)))
            if len(discount) == 2:
                fl_discount = '0.'+discount
                fl_discount = float(fl_discount)
            else:
                fl_discount = "0.0" + discount
                fl_discount = float(fl_discount)
            print('fl_discount ', fl_discount)

            if brutto_float < 100.00:
                cena_sprzedazy_brutto = round(old_price + (old_price * marza_do_100) ,1)

            elif brutto_float >= 400.00:
                cena_sprzedazy_brutto = round(old_price + (old_price * marza_od_400), 1)

            elif brutto_float >= 300.00:
                cena_sprzedazy_brutto = round(old_price + (old_price * marza_300_400), 1)

            elif brutto_float >= 200.00:
                cena_sprzedazy_brutto = round(old_price + (old_price * marza_200_300), 1)

            elif brutto_float >= 100.00:
                cena_sprzedazy_brutto = round(old_price + (old_price * marza_100_200), 1)
            print('Cena sprzedazy produkt %: ', cena_sprzedazy_brutto)



            discount_amount = round(poprzednia_cena_sprzedazy_brutto - (poprzednia_cena_sprzedazy_brutto * fl_discount),1)
            print('discount amount: ', discount_amount)
            print (discount +"%")
            #discount = str(d) + "%"
        else:
            discount = ""
            discount_amount = ""


        td_typ = params.find_all('td')
        for result in td_typ:
            if result.string == "Typ":
                typ = result.find_next('td').text.encode("utf-8")
                #print('Typ: ", typ
            #else:
            #   typ = ''

        td_wiek = params.find_all('td')
        for result in td_wiek:
            if result.string == "Dla dzieci w wieku od":
                wiek = result.find_next('td').text.encode("utf-8")
                #print wiek

        td_kategoria = params.find_all('td')
        for result in td_kategoria:
            k = result.string.find('Kategoria')
            if k != -1:
                kategoria = result.find_next('td').text.encode("utf-8")
                #print kategoria
            #else:
            #   kategoria = ''

        td_material = params.find_all('td')
        for result in td_material:
            m = result.string.find('materia')
            if m != -1:
                material = result.find_next('td').text.encode('utf-8')


        td_kolor = params.find_all('td')
        for result in td_kolor:
            if result.string == "Kolor":
                kolor = result.find_next('td').text.encode('utf-8')
                #print kolor
                #print(result.parent.text)    # wartosci z obu <td>


        td_waga = params.find_all('td')
        for result in td_waga:
            if result.string == "Waga jednostkowa brutto":
                waga = result.find_next('td').text
                #print waga

        td_wymiar = params.find_all('td')
        for result in td_wymiar:
            if result.string == "Wymiar opakowania jednostkowego (SxWxG)":
                wymiar = result.find_next('td').text
                wymiar = wymiar.replace(',', '.')
                print (wymiar)

        td_l_elementow = params.find_all('td')
        for result in td_l_elementow:
            m = result.string.find('Liczba element')
            if m != -1:
                elementy = result.find_next('td').text
                #print elementy

        URLRewritten = title.replace(' ','-')

        #url_image =extract_product_images_soup(item_name)



    #baza = [count, title, code, marka, old_price, netto_float, brutto_float, cena_sprzedazy_brutto, discount, discount_amount, wiek, typ, kategoria,
     #       kolor, waga, wymiar, material, elementy, short_desc]
    baza = [count, title, code, marka, old_price, netto_float, brutto_float, cena_sprzedazy_brutto, discount,
            discount_amount, wiek, typ, kategoria,
            kolor, waga, wymiar, material, elementy, short_desc]
    baza_list = []
    baza_list.append(baza)
    #print baza_list
    mysql_fun.insert_products(baza_list)


get_data_save_CSV(url_product2)

def main_spider(max_page):

    for num in range(1,max_page+1):
        #utworzenie nowego stringa przechowujacego ziterowane adresy stron do przetworzenia
        url_klocki_new = url_klocki + '?pageNo=' + str(num)
        print (url_klocki_new)
        #extract_thumbnail_images(url_klocki_new)

        source_code = requests.get(url_klocki_new)
        soup = BeautifulSoup(source_code.content, "html.parser")
        count = 0
        for link in soup.find_all('article', class_='small-product'):
            url = "http://www.selgros24.pl"
            a = link.findAll('a')[0].get('href')
            href = url + a
            #print href
            count = count + 1

            #zapisywanie danych do pliku csv
            get_data_save_CSV(href)

            #zapisywanie zdjec z funkcji
            extract_product_images(href)


        print('Pobrano produktow : ', count)

##funkcja przechodzaca przez wszystie produkty na wszystkich podstronach, ktora generuje csv z lista produktow ze strony (selgros24)
#main_spider(get_max_category_pages(url_klocki))





'''
try:
    os.remove(destinationPath+csvfile_features)
except OSError:
    pass
try:
    os.remove(destinationPath+csvfile_data)
except OSError:
    pass
'''

'''
#czyszczenie tabeli MySQL z produktami
mysql_fun.delete_products()
#czysczenie tabeli MySQL ze zdjeciami
mysql_fun.delete_images()
#Czysczenie folderu /img/logo ze zdjeciami
#functions.earse_directory_www()
#Czysczenie folderu /selgros/products_images ze zdjeciami
functions.earse_directory_products_images()

main_spider(get_max_category_pages(url_klocki))

'''

#Pobiera produkty z pierwszej strony
#main_spider(3)


#csv_functions.CSV_joinFiles('headers.csv', 'products_data.csv', 'products_ALL.csv')

#csv_functions.JoinHeaderProducts('produkty.csv', 'produkty2.csv')

#csv_functions.JoinHeaderProducts(csvfile_output, csvfile)


