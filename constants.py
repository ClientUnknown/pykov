import json
import zlib
import requests

GAME_VERSION = "0.12.3.5834"
LAUNCHER_VERSION = "0.9.3.1023"
UNITY_VERSION = "2018.4.13f1"

LAUNCHER_ENDPOINT = "https://launcher.escapefromtarkov.com"
PROD_ENDPOINT = "https://prod.escapefromtarkov.com"
TRADING_ENDPOINT = "https://trading.escapefromtarkov.com"
RAGFAIR_ENDPOINT = "https://ragfair.escapefromtarkov.com"

def check_launcher_version():
    global LAUNCHER_VERSION, LAUNCHER_ENDPOINT
    url = "{}/launcher/GetLauncherDistrib".format(LAUNCHER_ENDPOINT)
    body = {}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'BSG Launcher {}'.format(LAUNCHER_VERSION)
    }
    content = None

    rsp = requests.post(url, json=body, headers=headers)
    try:
        content = zlib.decompress(rsp.content).decode()
    except:
        pass

    if not content:
        print("check_launcher_version request failed: {}".format(rsp.status_code))
    elif rsp.status_code != 200:
        print("Could not get launcher version; error: {}".format(content))
    else:
        content = json.loads(content)
        version = content["data"]["Version"]
        if version != LAUNCHER_VERSION:
            LAUNCHER_VERSION = version
            print("Got current launcher version: {}".format(version))

def check_game_version():
    global LAUNCHER_ENDPOINT, LAUNCHER_VERSION, GAME_VERSION
    url = "{}/launcher/GetPatchList?launcherVersion={}&branch=live".format(
        LAUNCHER_ENDPOINT, LAUNCHER_VERSION
    )
    body = {}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'BSG Launcher {}'.format(LAUNCHER_VERSION)
    }
    content = None

    rsp = requests.post(url, json=body, headers=headers)
    try:
        content = zlib.decompress(rsp.content).decode()
    except:
        pass

    if not content:
        print("check_game_version request failed: {}".format(rsp.status_code))
    elif rsp.status_code != 200:
        print("Could not get game version; error: {}".format(content))
    else:
        content = json.loads(content)
        version = content["data"][0]["Version"]
        if version != GAME_VERSION:
            GAME_VERSION = version
            print("Got current game version: {}".format(GAME_VERSION))