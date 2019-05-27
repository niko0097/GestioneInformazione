#!/usr/bin/env python3

from distutils.core import setup
import os
import sys

setup(name='GestioneInformazione',
      version='1.0',
      description='Graphical search engine dblp',
      url='https://github.com/niko0097/GestioneInformazione',
      packages=['GestioneInformazione'],
     )

os.system("sudo cp supersearch /usr/local/bin")

if (sys.argv[1] == 'install'):
    print('\n\nGestioneInformazione installed successfully.' +
        '\n\n\t- supersearch\t\tStart the graphical search engine.' +
        '\n\nBUG Report: https://github.com/niko0097/GestioneInformazione\n')
