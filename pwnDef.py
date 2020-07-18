#!/usr/bin/env python
import sys
import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pdb

parser = 'lxml'

visible = ['Wielki słownik ortograficzny PWN',
        'Słownik języka polskiego PWN',
        'Encyklopedia PWN']

try:
    word = sys.argv[1]
    defs = SoupStrainer('div', class_='entry ')
    soup = BeautifulSoup(requests.get('https://sjp.pwn.pl/szukaj/' + word + '.html').content,
            features=parser, parse_only=defs)
    results = soup.find_all('div', class_='entry')
    for result in results:
        title = result.contents[1].get_text()
        if title in visible:
            print(title + '\n')
            definitions = result.contents[3]
            items = definitions.find_all('div', class_='ribbon-element')
            for item in items:
                print(item.get_text() + '\n')
except IndexError:
    print('syntax: pwndef <word>')
