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


APPDATA_DIR = str(pathlib.Path.home()) + "\\AppData\\Roaming\\"
MC_DIRECTORY = str(pathlib.Path.home()) + "\\AppData\\Roaming\\.minecraft\\"
VP_DIRECTORY = str(pathlib.Path.home()) + "\\AppData\\Roaming\\.vicepack\\"
MC_VERSIONS = MC_DIRECTORY + "versions\\"
MC_MODS = VP_DIRECTORY + "mods\\"
URL_MODPACK = "http://185.25.207.152/"
SHA_256_FILE = "3C94832DAC61DCFA4AF3144514B8BEDEF80A0BF81FA6F03132122BBB71781D63"
MC_PROFILE = {
    "name" : "VicePack - Original",
    "gameDir" : VP_DIRECTORY,
    "lastVersionId": "1.7.10-Forge10.13.4.1614-1.7.10",
    "javaArgs": "-Xmx4G -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy -Xmn128M"
}
TEMPLATE_INSTALLED_VS = {
    "versionInstalled" : "null"
}
FILE_LIST_VP = ['config.json'] 



def install_data(zipFile):
    """It extracts all the files and install all of them"""
    print("\nEstraggo i file dallo zip.. ", end='')
    with zipfile.ZipFile(VP_DIRECTORY + zipFile, "r") as file:
        file.extractall(VP_DIRECTORY)
    print("Fatto\nControllo le versioni di minecraft installate.. ")
    
    if os.path.exists(MC_VERSIONS + "1.7.10"):
        print("-> 1.7.10 OK")
    else:
        print("-> 1.7.10 Non presente, installo.. ", end='')
        os.rename(VP_DIRECTORY + "VicePack_Original\\forge\\1.7.10 ", MC_VERSIONS + "1.7.10")
        print("Fatto!")

    if os.path.exists(MC_VERSIONS + "1.7.10-Forge10.13.4.1614-1.7.10"):
        print("-> 1.7.10-Forge10.13.4.1614-1.7.10 OK")
    else:
        print("-> 1.7.10-Forge10.13.4.1614-1.7.10 Non presente, installo.. ", end='')
        os.rename(VP_DIRECTORY + "VicePack_Original\\forge\\1.7.10-Forge10.13.4.1614-1.7.10", MC_VERSIONS + "\\1.7.10-Forge10.13.4.1614-1.7.10")
        print("Fatto!")
    
    print("Controllo cartella mods..")
    ALL_MODS = os.listdir(VP_DIRECTORY + "VicePack_Original\\mods\\")
    PATH_MODS = VP_DIRECTORY + "VicePack_Original\\mods\\"
    if os.path.exists(MC_MODS):
        shutil.rmtree(MC_MODS)
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
    shutil.rmtree(VP_DIRECTORY + "VicePack_Original")
    print("Fatto!")


def __ctrl_hash(hash, filed):
    """It controls the hash of the zip file"""
    file_hash = hashlib.sha256()
    with open(VP_DIRECTORY + filed, "rb") as file:
        fb = file.read(65536)
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = file.read(65536)
        file.close()
    if file_hash.hexdigest().upper() == hash:
        print("Hash Verificato! Il file è integro!")
    else:
        print("Hash non verificato, errore! Probabile manomissione del file!")


def download_modpack(ver, hash, filed):
    """It downloads all the files from the mirror"""
    try:
        urllib.request.urlretrieve(ver, VP_DIRECTORY + filed)
    except urllib.error.HTTPError:
        print("\nLink del mirror non risponde.. Esco")
        exit(-1)
    print("OK\nEseguo l'hash del modpack.. ", end='')
    __ctrl_hash(hash, filed)


def modify_json_shignima():
    """It loads the json config file made by Shignima Laucher"""

    try:
        file = open(MC_DIRECTORY + "launcher_profiles.json", "r")
        config_file = json.load(file)
        file.close()

        config_file["profiles"]["VicePack - Original"] = MC_PROFILE
        config_file["selectedProfile"] = "VicePack - Original"

        file = open(MC_DIRECTORY + "launcher_profiles.json", "w+")
        file.write(json.dumps(config_file, indent=4))
        file.close()
        print("Aggiunto pacchetto al launcher!")
        
    except FileNotFoundError:
        print("File 'launcher_profiles.json' non trovato nella directory")


def check_vicepack_version():
    """It checks the vicepack version installed, if it is installed"""
    print("\nControllo versione installata di VicePack.. ", end='')
    if os.path.exists(VP_DIRECTORY + "config.json"):
        file = open(VP_DIRECTORY + "config.json", "r")
        conf_file = json.load(file)
        file.close()
        
        file = open(VP_DIRECTORY + "releases.json", "r")
        release_file = json.load(file)
        file.close()
        
        if conf_file['versionInstalled'] == 'null':
            print("Nessuna versione installata.. \nUltima versione rilasciata: ", end='')
            
            versions = list(dict.keys(release_file['versions']))
            for i in versions:
                if release_file['versions'][i]['isLastRelease'] == "yes":
                    print(i + ".. Download dell'ultima versione dal mirror.. ", end='')
                    download_modpack(URL_MODPACK + release_file['versions'][i]['zipFile'],
                        release_file['versions'][i]['sha256'], str(release_file['versions'][i]['zipFile']).replace("files/", ""))
                    install_data(release_file['versions'][i]['zipFile'].replace("files/", ""))
                    break
            conf_file['versionInstalled'] = i
            file = open(VP_DIRECTORY + "config.json", "w+")     
            file.write(json.dumps(conf_file, indent=4))
            file.close()
            print("Versione " + i + " scaricata con successo")
            rm_files(str(release_file['versions'][i]['zipFile']).replace("files/", ""))
        else:
            print("Versione Installata: " + conf_file['versionInstalled'])
            print("Controllo se sono presenti aggiornamenti.. Ultima versione rilasciata: ", end='')
            versions = list(dict.keys(release_file['versions']))
            for i in versions:
                if release_file['versions'][i]['isLastRelease'] == "yes":
                    print(i)
                    if conf_file['versionInstalled'] == i:
                        print("\u001b[32m\nNessun aggiornamento trovato!\u001b[0m")
                        break
                    else:
                        print("Trovato aggiornamento, versione " + i + "Download dell'ultimo aggiornamento.. ", end='')
                        download_modpack(URL_MODPACK + release_file['versions'][i]['zipFile'],
                            release_file['versions'][i]['sha256'], str(release_file['versions'][i]['zipFile']).replace("files/", ""))
                        install_data(str(release_file['versions'][i]['zipFile']).replace("files/", ""))
                        print("\u001b[32m\nVersione " + i + " scaricata con successo\u001b[0m")
                        conf_file['versionInstalled'] = i
                        file = open(VP_DIRECTORY + "config.json", "w+")     
                        file.write(json.dumps(conf_file, indent=4))
                        file.close()
                        rm_files(str(release_file['versions'][i]['zipFile']).replace("files/", ""))
                        break
    else:
        print("\nErrore: file 'config.json' non trovato dopo il precedente controllo.")
        exit(-1)


def download_releases_json():
    print("\nDownload in corso di releases.json dal mirror.. ", end='')
    try:
        urllib.request.urlretrieve(URL_MODPACK + "files/json/releases.json",
            VP_DIRECTORY + "releases.json")
    except urllib.error.HTTPError:
        print("\nLink del mirror non risponde.. Esco")
        exit(-1)
    print("OK")


def rm_files(zipFile):
    os.remove(VP_DIRECTORY + "releases.json")
    os.remove(VP_DIRECTORY + zipFile)


def create_config():
    with open(VP_DIRECTORY + "config.json", "w+")as file:
        file.write(json.dumps(TEMPLATE_INSTALLED_VS, indent=4))
        file.close()


def setup_vicepack():
    # Controllo se la cartella .vicepack è presente
    print("Controllo se VicePack è stato installato.. ", end='')
    if not os.path.exists(APPDATA_DIR + "\\.vicepack"):
        print("Installazione non trovata\nCreo le impostazioni del launcher..", end='')
        os.mkdir(APPDATA_DIR + "\\.vicepack")
        create_config()
        print("OK")
        modify_json_shignima()
    else:
        print("Installazione trovata\nControllo integrità dei file.. ", end='')
        file_list = os.listdir(APPDATA_DIR + "\\.vicepack")
        for file in FILE_LIST_VP:
            print("\n--> " + file + ".. ", end='')    
            if not file in file_list:
                print("Non presente, creo il file.. ", end='')
                create_config()
                print("OK")
            else:
                print("OK")
    
    # Controllo se le impostazioni del launcher di Shigninima sono modificate
    print("\nControllo se VicePack è stato installato nelle impostazioni del launcher... ")
    try:
        with open(MC_DIRECTORY + "launcher_profiles.json", 'r+') as file:
            print("--> launcher_profiles.json.. " , end='')
            setting = json.load(file)
            if not "VicePack - Original" in setting['profiles']:
                modify_json_shignima()
            else:
                print("OK")
    except FileNotFoundError:
        print("\nIl file 'launcher_profiles.json' non è stato trovato. " +
            "Sei sicuro di aver aperto il launcher?")


if __name__ == "__main__":
    print(u"\u001b[33mVicePack Installer - Versione 1.2\u001b[0m\n")
    setup_vicepack()
    download_releases_json()
    check_vicepack_version()
