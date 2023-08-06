#!/usr/bin/env python

import os
import sys
from distutils.core import setup
from setuptools import find_packages


def get_version():
    return open('version.txt', 'r').read().strip()


setup(
    author='Nicollas Neumann Borges',
    author_email='nicollasborges@lojaspompeia.com.br',
    description='Pacote de envio de email',
    license='MIT',
    name='lins_mail_sender',
    packages=find_packages(),
    url='https://bitbucket.org/grupolinsferrao/pypck-lins-mail-sender/',
    version=get_version()
)
