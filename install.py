"""
VicePack installer

@author: Elia Vicentini <eliavicentini26@gmail.com>
"""

import json
import pathlib
import os
import urllib.request
import hashlib
import zipfile
import shutil


MC_DIRECTORY = str(pathlib.Path.home()) + "\\AppData\\Roaming\\.minecraft\\"
MC_VERSIONS = MC_DIRECTORY + "versions\\"
MC_MODS = MC_DIRECTORY + "mods\\"
MC_PROFILE = {
    "name" : "VicePack - Original",
    "lastVersionId": "1.7.10-Forge10.13.4.1614-1.7.10",
    "javaArgs": "-Xmx4G -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy -Xmn128M"
}
URL_MODPACK = "http://185.25.207.152/files/VicePack_Original_1_0.zip"
SHA_256_FILE = "3C94832DAC61DCFA4AF3144514B8BEDEF80A0BF81FA6F03132122BBB71781D63"


def install_data():
    """It extracts all the files and install all of them"""
    print("Estraggo i file dallo zip.. ", end='')
    with zipfile.ZipFile("download\\VicePack_Original_1_0.zip", "r") as file:
        file.extractall(".\\download")
    print("Fatto\nControllo le versioni di minecraft installate.. ")
    
    if os.path.exists(MC_VERSIONS + "1.7.10"):
        print("-> 1.7.10 OK")
    else:
        print("-> 1.7.10 Non presente, installo.. ", end='')
        os.rename("download\\VicePack_Original\\forge\\1.7.10 ", MC_VERSIONS + "\\1.7.10")
        print("Fatto!")

    if os.path.exists(MC_VERSIONS + "1.7.10-Forge10.13.4.1614-1.7.10"):
        print("-> 1.7.10-Forge10.13.4.1614-1.7.10 OK")
    else:
        print("-> 1.7.10-Forge10.13.4.1614-1.7.10 Non presente, installo.. ", end='')
        os.rename("download\\VicePack_Original\\forge\\1.7.10-Forge10.13.4.1614-1.7.10", MC_VERSIONS + "\\1.7.10-Forge10.13.4.1614-1.7.10")
        print("Fatto!")
    
    print("Controllo cartella mods..")
    ALL_MODS = os.listdir("download\\VicePack_Original\\mods\\")
    PATH_MODS = "download\\VicePack_Original\\mods\\"
    if os.path.exists(MC_MODS):
        files = os.listdir(MC_MODS)
        for mod in ALL_MODS:
            print("-> " + str(mod) + ".. ", end='')
            if mod in files:
                print("OK")
            else:
                print("Non presente, installo.. ", end='')
                os.rename(PATH_MODS + mod, MC_MODS + mod)
                print("Fatto!")
    else:
        os.mkdir(MC_MODS)
        files = os.listdir(MC_MODS)
        for mod in ALL_MODS:
            print("-> " + str(mod) + ".. ", end='')
            if mod in files:
                print("OK")
            else:
                print("Non presente, installo.. ", end='')
                os.rename(PATH_MODS + mod, MC_MODS + mod)
                print("Fatto!")

    print("Elimino i file del programma.. ", end='')
    shutil.rmtree("download")
    print("Fatto! Ora sei pronto per giocare!")


def ctrl_hash():
    """It controls the hash of the zip file"""
    file_hash = hashlib.sha256()
    with open("download\\VicePack_Original_1_0.zip", "rb") as file:
        fb = file.read(65536)
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = file.read(65536)
        file.close()
    if file_hash.hexdigest().upper() == SHA_256_FILE:
        print("Hash Verificato! Il file è integro!")
    else:
        print("Hash non verificato, errore! Probabile manomissione del file!")


def download_data():
    """It installs all the mod of the modpack, config included"""
    
    try:
        print("Controllo se la cartella download è presente.. ", end='')
        if not os.path.exists("download"):
            print("Non presente, creo la cartella download")
            os.mkdir("download")
            print("Controllo se il modpack è già stato scaricato.. ", end='')
            if not os.path.exists("download\\VicePack_Original_1_0.zip"):
                print("Modpack non presente, download in corso.. ", end='')
                urllib.request.urlretrieve(URL_MODPACK, "download\\VicePack_Original_1_0.zip")
                print("Download effettuato!\nVerifico hash modpack.. ", end='')
                ctrl_hash()
            else:
                print("Modpack già scaricato!\nVerifico hash modpack.. ", end='')
                ctrl_hash()
        else:
            print("Cartella download esistente\nControllo se il modpack è già stato scaricato.. ", end='')
            if not os.path.exists("download\\VicePack_Original_1_0.zip"):
                print("Modpack non presente, download in corso.. ", end='')
                urllib.request.urlretrieve(URL_MODPACK, "download\\VicePack_Original_1_0.zip")
                print("Download effettuato!\nVerifico hash modpack.. ", end='')
                ctrl_hash()
            else:
                print("Modpack già scaricato!\nVerifico hash modpack.. ", end='')
                ctrl_hash()
    except FileExistsError:
        os.rmdir("download")


def modify_json_shignima():
    """It loads the json config file made by Shignima Laucher"""

    try:
        print("Aggiungo al tuo launcher il nuovo pacchetto.. ", end='')
        file = open(MC_DIRECTORY + "launcher_profiles.json", "r")
        config_file = json.load(file)
        file.close()

        config_file["profiles"]["VicePack - Original"] = MC_PROFILE
        config_file["selectedProfile"] = "VicePack - Original"

        file = open(MC_DIRECTORY + "launcher_profiles.json", "w+")
        file.write(json.dumps(config_file, indent=4))
        file.close()
        print("Fatto!")
        
    except FileNotFoundError:
        print("File 'launcher_profiles.json' non trovato nella directory")


if __name__ == "__main__":
    print("VicePack Installer - Versione 1.0\n") 
    modify_json_shignima()
    download_data()
    install_data()
