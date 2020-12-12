"""
VicePack installer

@author: Elia Vicentini <eliavicentini26@gmail.com>
"""

import json
import pathlib
import os
import requests
import urllib.request
import hashlib
import zipfile
import shutil


APPDATA_DIR = str(pathlib.Path.home()) + "\\AppData\\Roaming\\"
MC_DIRECTORY = str(pathlib.Path.home()) + "\\AppData\\Roaming\\.minecraft\\"
VP_DIRECTORY = str(pathlib.Path.home()) + "\\AppData\\Roaming\\.vicepack\\"
MC_VERSIONS = MC_DIRECTORY + "versions\\"
MC_MODS = VP_DIRECTORY + "mods\\"
MC_CONF = VP_DIRECTORY + "config\\"
URL_MODPACK = "http://185.25.207.152/"
URL_INSTALLER_RELEASE = "https://api.github.com/repos/IlVice26/vicepack-installer/releases/latest"
SHA_256_FILE = "3C94832DAC61DCFA4AF3144514B8BEDEF80A0BF81FA6F03132122BBB71781D63"
MC_PROFILE = {
    "name" : "VicePack - Original",
    "gameDir" : VP_DIRECTORY,
    "lastVersionId": "1.7.10-Forge10.13.4.1614-1.7.10",
    "javaArgs": "-Xmx4G -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy -Xmn128M"
}
TEMPLATE_INSTALLED_VS = {
    "versionInstalled" : "null",
    "installerVersion" : "null"
}
FILE_LIST_VP = {
    "main_dir" : [
        'config.json'
    ],
    "conf_dir" : [
        'CustomMainMenu\\mainmenu.json'
    ]
} 


def install_data(zipFile, tag):
    """It extracts all the files and install all of them"""
    print("\nEstraggo i file dallo zip.. ", end='')
    with zipfile.ZipFile(VP_DIRECTORY + zipFile, "r") as file:
        file.extractall(VP_DIRECTORY)
    
    if tag == "lastRelease":
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
        files = os.listdir(MC_MODS)
        for mod in ALL_MODS:
            print("-> " + str(mod) + ".. ", end='')
            if mod in files:
                print("\u001b[32mOK\u001b[0m")
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
                print("\u001b[32mOK\u001b[0m")
            else:
                print("Non presente, installo.. ", end='')
                os.rename(PATH_MODS + mod, MC_MODS + mod)
                print("Fatto!")

    print("Elimino i file del programma.. ", end='')
    shutil.rmtree(VP_DIRECTORY + "VicePack_Original")
    os.remove(VP_DIRECTORY + str(zipFile).replace("files/", ""))
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
        print("\u001b[31mHash non verificato, errore! Probabile manomissione del file!\u001b[0m")
        print("\nSHA256 su releases.json: " + file_hash.hexdigest().upper()
            + "\nSHA256 di " + filed + ": " + hash)
        print("\nContatta <eliavicentini26@gmail.com> per risolvere il problema!")
        exit(-1)


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

        file = open(MC_CONF + "CustomMainMenu\\mainmenu.json", "r")
        menu_file = json.load(file)
        file.close()

        temp_versions = []
        updates = [] 
        lastRelease = "null"
        versions = list(dict.keys(release_file['versions']))
        for i in versions:
            temp_versions.append(i)
            if release_file["versions"][i]["isLastRelease"] == "yes":
                lastRelease = i

        for i in range(temp_versions.index(lastRelease) + 1, len(temp_versions)):
            updates.append(temp_versions[i])

        if conf_file['versionInstalled'] == 'null':
            print("Nessuna versione installata.. \nUltima versione rilasciata: " + lastRelease)
            print("Download dell'ultima versione dal mirror.. ", end='')
            download_modpack(URL_MODPACK + release_file['versions'][lastRelease]['zipFile'],
                            release_file['versions'][lastRelease]['sha256'], 
                            str(release_file['versions'][lastRelease]['zipFile']).replace("files/", ""))
            install_data(release_file['versions'][lastRelease]['zipFile'].replace("files/", ""), "lastRelease")

            if (len(updates) != 0):
                print("Aggiornamenti del modpack da installare: " + str(len(lastRelease)))
                for update in updates:
                    if not update == conf_file['versionInstalled']:
                        print("\nDownload dell'update " + update + " in corso.. ", end='')
                        download_modpack(URL_MODPACK + release_file['versions'][update]['zipFile'],
                                        release_file['versions'][update]['sha256'], 
                                        str(release_file['versions'][update]['zipFile']).replace("files/", ""))
                        install_data(release_file['versions'][update]['zipFile'].replace("files/", ""), "update")
                        print("\u001b[32m\nVersione " + update + " scaricata con successo\u001b[0m")

                # Update dei valori
                menu_file["texts"]["info-modpack"]["text"] = "Vicepack: " + updates[-1] 
                conf_file['versionInstalled'] = updates[-1]

                # Update della versione in config.json
                file = open(VP_DIRECTORY + "config.json", "w+")     
                file.write(json.dumps(conf_file, indent=4))
                file.close()

                # Update della versione in mainmenu.json
                file = open(MC_CONF + "CustomMainMenu\\mainmenu.json", "w+")
                file.write(json.dumps(menu_file, indent=4))
                file.close()
            else:
                conf_file['versionInstalled'] = lastRelease
                file = open(VP_DIRECTORY + "config.json", "w+")     
                file.write(json.dumps(conf_file, indent=4))
                file.close()
        else:
            print("Versione Installata: " + conf_file['versionInstalled'])
            print("Controllo se sono presenti aggiornamenti.. ", end='')
            
            if (len(updates) != 0):
                if conf_file['versionInstalled'] == updates[-1]:
                    print("\u001b[32m\n\nNessun aggiornamento trovato!\u001b[0m")
                else:
                    print("Aggiornamenti trovati: " + str(len(temp_versions) - 1 
                        - temp_versions.index(conf_file['versionInstalled'])))
                    for update in updates:
                        if not update == conf_file['versionInstalled']:
                            print("\nDownload dell'update " + update + " in corso.. ", end='')
                            download_modpack(URL_MODPACK + release_file['versions'][update]['zipFile'],
                                release_file['versions'][update]['sha256'], str(release_file['versions'][update]['zipFile']).replace("files/", ""))
                            install_data(release_file['versions'][update]['zipFile'].replace("files/", ""), 
                            "update")
                            print("\u001b[32m\nVersione " + update + " scaricata con successo\u001b[0m")

                    # Update dei valori
                    menu_file["texts"]["info-modpack"]["text"] = "Vicepack: " + updates[-1] 
                    conf_file['versionInstalled'] = updates[-1]

                    # Update della versione in config.json
                    file = open(VP_DIRECTORY + "config.json", "w+")     
                    file.write(json.dumps(conf_file, indent=4))
                    file.close()

                    # Update della versione in mainmenu.json
                    file = open(MC_CONF + "CustomMainMenu\\mainmenu.json", "w+")
                    file.write(json.dumps(menu_file, indent=4))
                    file.close()
            else:
                print("\u001b[32m\n\nNessun aggiornamento trovato!\u001b[0m")
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
    print("\u001b[32mOK\u001b[0m")


def download_cmm_data():

    if not os.path.exists(VP_DIRECTORY + "config\\CustomMainMenu"):
        os.mkdir(VP_DIRECTORY + "config\\CustomMainMenu")
    try:
        urllib.request.urlretrieve(URL_MODPACK + "files/json/mainmenu.json",
            VP_DIRECTORY + "config\\CustomMainMenu\\mainmenu.json")
    except urllib.error.HTTPError:
        print("\nLink del mirror non risponde.. Esco")
        exit(-1)
    
    try:
        urllib.request.urlretrieve(URL_MODPACK + "files/custommainmenu.zip",
            VP_DIRECTORY + "custommainmenu.zip")
    except urllib.error.HTTPError:
        print("\nLink del mirror non risponde.. Esco")
        exit(-1)
    with zipfile.ZipFile(VP_DIRECTORY + "custommainmenu.zip", "r") as file:
        file.extractall(VP_DIRECTORY + "resources\\")
        os.remove(VP_DIRECTORY + "custommainmenu.zip")


def rm_files():
    os.remove(VP_DIRECTORY + "releases.json")


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
        print("\u001b[32mOK\u001b[0m")
        modify_json_shignima()
    else:
        print("Installazione trovata\nControllo integrità dei file.. ")

        # Files in FILE_LIST_VP
        main_dir_files = FILE_LIST_VP["main_dir"]
        conf_dir_files = FILE_LIST_VP["conf_dir"]

        # Ctrl for files in VP_DIRECTORY
        for file in main_dir_files:
            print("--> " + file + ".. ", end='')    
            if not os.path.exists(VP_DIRECTORY + file):
                    print("Non presente, creo il file.. ", end='')
                    create_config()
                    print("\u001b[32mOK\u001b[0m")
            else:
                if file == "config.json":
                    file_config = open(VP_DIRECTORY + "config.json", "r")
                    conf = json.load(file_config)
                    file_config.close()

                    actual_conf = conf.keys()
                    template_conf = TEMPLATE_INSTALLED_VS.keys()

                    for line in template_conf:
                        if line not in actual_conf:
                            conf[line] = "null"
                            file_config = open(VP_DIRECTORY + "config.json", "w")
                            file_config.write(json.dumps(conf, indent=4))
                            file_config.close()
                            break
                    print("\u001b[32mOK\u001b[0m")
                else:
                    print("\u001b[32mOK\u001b[0m")

        # Ctrl files in Config dir of VP_DIRECTORY
        for file in conf_dir_files:
            print("--> " + file + ".. ", end='')
            if not os.path.exists(MC_CONF + file):
                print("Non scaricato, scarico i dati.. ", end='')
                download_cmm_data()
                print("\u001b[32mOK\u001b[0m")
            else:
                print("\u001b[32mOK\u001b[0m")
    
    # Controllo se le impostazioni del launcher di Shigninima sono modificate
    print("\nControllo se VicePack è stato installato nelle impostazioni del launcher... ")
    try:
        with open(MC_DIRECTORY + "launcher_profiles.json", 'r+') as file:
            print("--> launcher_profiles.json.. " , end='')
            setting = json.load(file)
            if not "VicePack - Original" in setting['profiles']:
                modify_json_shignima()
            else:
                print("\u001b[32mOK\u001b[0m")
    except FileNotFoundError:
        print("\nIl file 'launcher_profiles.json' non è stato trovato. " +
            "Sei sicuro di aver aperto il launcher?")


def check_vicepack_installer():
    response = requests.get(URL_INSTALLER_RELEASE)
    tag = response.json()["tag_name"]
    update_url = response.json()["assets"][0]["browser_download_url"]
    update_file = str(response.json()["assets"][0]["browser_download_url"]).split("/")[-1]

    file = open(VP_DIRECTORY + "config.json", "r")
    config = json.load(file)
    file.close()

    if config['installerVersion'] == "null":
        print("\nVersione dell'installer sconosciuta.. " 
            + "Ultima versione rilasciata su: " + tag)

        try:
            print("Download della versione: " + tag + " in corso.. ", end='')
            urllib.request.urlretrieve(update_url, update_file)
        except urllib.error.HTTPError:
            print("Impossibile scaricare l'aggiornamento")
        print("\u001b[32mOK\u001b[0m")

        file = open(VP_DIRECTORY + "config.json", "w")
        config['installerVersion'] = tag
        file.write(json.dumps(config, indent=4))
        file.close()

        print("\nupdater.py installerà l'aggiornamento!" +
            " E' solo una questione di secondi!")

        os.system("updater.py")
        exit(0)

    elif config['installerVersion'] == tag:
        print("\u001b[32m\nNessun aggiornamento trovato dell installer!" +
            "\nVersione installata: " + tag + "\u001b[0m")
    else:
        print("\nVersione dell'installer: " + config['installerVersion']
            + ", Ultima versione rilasciata su Github: " + tag)
        
        try:
            print("Download della versione: " + tag + " in corso.. ", end='')
            urllib.request.urlretrieve(update_url, update_file)
        except urllib.error.HTTPError:
            print("Impossibile scaricare l'aggiornamento")
        print("\u001b[32mOK\u001b[0m")

        file = open(VP_DIRECTORY + "config.json", "w")
        config['installerVersion'] = tag
        file.write(json.dumps(config, indent=4))
        file.close()

        print("\nupdater.py installerà l'aggiornamento!" +
            " E' solo una questione di secondi!")

        os.system("updater.py")
        exit(0)


if __name__ == "__main__":
    os.system("cls")
    print(u"\u001b[33mVicePack Installer - Versione 1.4.1\u001b[0m\n")
    setup_vicepack()
    check_vicepack_installer()
    download_releases_json()
    check_vicepack_version()
    rm_files()
