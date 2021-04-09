#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from ms_access_to_csv import converter
from npri_scraper import scraper

if __name__ == '__main__':
    scraper()
    converter()
