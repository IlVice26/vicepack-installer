"""
VicePack installer - Updater

@author: Elia Vicentini <eliavicentini26@gmail.com>
"""

import os
import shutil
import zipfile
import time


def unzip_files():
    
    if os.path.exists("temp"):
        shutil.rmtree("temp")
        os.mkdir("temp")
    else:
        os.mkdir("temp")
    
    print("Unzip della release.. ", end='')
    with zipfile.ZipFile("vicepack_installer.zip", "r") as file:
        file.extractall("temp")
    print("\u001b[32mOK\u001b[0m\n\nCopia dei file nella directory")

    files = os.listdir("temp")
    for file in files:
        if file != 'updater.py':
            print("--> " + file + ".. ", end='')
            shutil.move("temp\\" + file, file)
            print("\u001b[32mOK\u001b[0m")
    
    print("Pulizia dei file di aggiornamento.. ", end='')
    shutil.rmtree("temp")
    os.remove("vicepack_installer.zip")
    print("\u001b[32mOK\u001b[0m")

    print("\u001b[32m\nRiavvio dell'installer tra 5 secondi!" + 
        " Aggiornamento completato!\u001b[0m")
    time.sleep(5)
    os.system("cls")
    os.system("install.py")

if __name__ == "__main__":
    print(u"\u001b[33m\nVicePack Installer - Updater\u001b[0m\n")
    unzip_files()