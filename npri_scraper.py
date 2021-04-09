#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from bs4 import BeautifulSoup
import requests
import os, io
from common import config
import zipfile

def visit(url):
    '''
    Function to recover the website soup
    '''

    response  = requests.get(url)
    response.raise_for_status

    return BeautifulSoup(response.text, 'html.parser')


def extracting(soup, NPRI_zip, dir_path):
    '''
    Function to extract the .accdb file
    '''

    element = soup.select(NPRI_zip)[0]
    link = element['href']
    r_file = requests.get(link)
    with zipfile.ZipFile(io.BytesIO(r_file.content)) as z:
        z.extractall(dir_path)


def scraper():
    '''
    Funtion for retrieving the NPRI from the web
    '''

    dir_path = os.path.dirname(os.path.realpath(__file__))

    _config = config()['web_sites']['NPRI']
    _queries = _config['queries']
    _url = _config['url']

    soup = visit(_url)
    extracting(soup, _queries['NPRI_zip'], dir_path)
