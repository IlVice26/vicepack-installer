"""
VicePack installer - Releases Updater

@author: Elia Vicentini <eliavicentini26@gmail.com>
"""

from zipfile import ZipFile
from os.path import basename

import urllib.request
import json
import os
import shutil
import time
import hashlib


def download_releases():
    try:
        print("Download di 'releases.json' in corso.. ", end='')
        urllib.request.urlretrieve("http://185.25.207.152/files/json/releases.json", "files/json/releases.json")
        print("OK")
    except urllib.error.HTTPError:
        print("Il server non risponde, controlla il server")


def update_releases():
    # Caricamento del json
    print("Caricamento di 'releases.json' in corso.. ", end='')
    file = open("files\\json\\releases.json", "r")
    config = json.load(file)
    file.close()
    print("OK")

    version = input(str("\nVersione: "))
    zipFile = "VicePack_Original_" + version.replace(".", "_")

    update = input(str("Questo è un aggiornamento?: ")).lower()

    if update.__contains__("y"):
        isAnUpdate = "yes"
        isLastRelease = "no"
    else:
        versions = list(dict.keys(config['versions']))
        for i in versions:
            if config['versions'][i]['isLastRelease'] == "yes":
                print(i)
                break
        config['versions'][i]['isLastRelease'] = 'no'
        isAnUpdate = "no"
        isLastRelease = "yes"

    # Creazione dello zip
    print("\nCreazione del file zip in corso.. ", end="")
    os.mkdir("files\\VicePack_Original")
    os.mkdir("files\\VicePack_Original\\VicePack_Original")
    shutil.copytree("files\\mods", "files\\VicePack_Original\\VicePack_Original\\mods")
    shutil.copytree("files\\forge", "files\\VicePack_Original\\VicePack_Original\\forge")
    shutil.make_archive("files\\" + zipFile, 'zip', 'files\\VicePack_Original')
    shutil.rmtree("files\\VicePack_Original")
    print("OK")

    # Hash of zipFile
    print("Hash del file zip in corso.. ", end='')
    file_hash = hashlib.sha256()
    with open("files\\" + zipFile + ".zip", "rb") as file:
        fb = file.read(65536)
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = file.read(65536)
        file.close()
    sha256 = file_hash.hexdigest().upper()
    print("OK")

    print("Creazione della lista delle mod in corso.. ", end='')
    modList = os.listdir("files\\mods")
    print("OK")

    changelog = input(str("\nChangelog: "))

    print("Creazione del nuovo 'releases.json'.. ", end='')
    config_dict = {
        "sha256" : sha256,
        "isLastRelease" : isLastRelease,
        "isAnUpdate" : isAnUpdate,
        "changelog" : changelog,
        "zipFile" : 'files/' + zipFile + '.zip',
        "modList" : modList
    }

    config["versions"][version] = config_dict

    file = open('files\\releases.json', 'w+')
    file.write(json.dumps(config, indent=4))
    file.close()
    print('OK')

    print("\u001b[32m\nI file sono pronti per essere caricati sul server!\u001b[0m")


if __name__ == "__main__":
    print(u"\u001b[33mVicePack Installer - Releases Updater\u001b[0m\n")
    download_releases()
    update_releases()