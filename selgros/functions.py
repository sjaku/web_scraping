#!/usr/bin/env python
import glob
import os

def earse_directory_products_images():
    directory='/Users/szymon/PycharmProjects/my_project/selgros/products_images/'
    os.chdir(directory)
    files=glob.glob('*.jpg')
    for filename in files:
        os.unlink(filename)


def earse_directory_www():
    directory='/Applications/XAMPP/xamppfiles/htdocs/sklep/img/lego/'
    os.chdir(directory)
    files=glob.glob('*.jpg')
    for filename in files:
        os.unlink(filename)