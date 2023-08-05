from setuptools import setup
import os

VERSION = '0.5'
VERS = VERSION.replace('.', '')

setup(
    name = 'clow',
    packages = ['clow'],
    version = VERSION,
    license = 'MIT',
    description = 'Clow Language',
    author = 'Yuri Rapoport',
    author_email = 'yuri.rapoport@gmail.com',
    url = 'https://github.com/yrapop01/clow',
    download_url = f'https://github.com/yrapop01/clow/archive/v_{VERS}.tar.gz',
    keywords = ['STATIC', 'TYPES', 'TYPING', 'INFERENCE'],
    install_requires = ['typehint'],
    classifiers = [
      'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
      'Intended Audience :: Developers', 
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
    ]
)
