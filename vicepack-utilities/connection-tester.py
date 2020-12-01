"""
VicePack installer - Connection Tester

@author: Elia Vicentini <eliavicentini26@gmail.com>
"""

import urllib.request
import os


def test_connection():
    try:
        urllib.request.urlretrieve("http://185.25.207.152/files/Prova.zip", "prova.zip")
        print("Download effettuato, il server risponde correttamente")
        os.remove("prova.zip")
    except urllib.error.HTTPError:
        print("Il server non rispnde, ripova")
    


if __name__ == "__main__":
    test_connection()