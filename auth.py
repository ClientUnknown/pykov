import requests
import json
import zlib
from hashlib import md5
from pykov import constants

# Object used to login and store session info
class Auth:
    def __init__(self, hwid):
        self.rsp = None
        self.sess = None
        self.hwid = hwid

    # Login to launcher with POST request; use 2fa if needed
    def login(self, email, password):
        url = "{}/launcher/login?launcherVersion={}&branch=live".format(
            constants.LAUNCHER_ENDPOINT, constants.LAUNCHER_VERSION
        )
        password = md5(password.encode('utf-8')).hexdigest()
        url = url.rstrip()
        self.hwid = self.hwid.rstrip()

        body = {"email":email, "pass":password, "hwCode":self.hwid, "captcha":""}
        headers = {
            'User-Agent': 'BSG Launcher {}'.format(constants.LAUNCHER_VERSION), 
            'Content-Type': 'application/json',
            'Content-Encoding': 'gzip' }
        cookies = {}

        self.rsp = requests.post(url, json=body, headers=headers, cookies=cookies)
        print("Login response code: {}".format(self.rsp.status_code))
        if self.rsp.status_code == 200:
            con = zlib.decompress(self.rsp.content).decode()
            if "Need confirm" in con:
                print("Need to authorize connection with 2fa")
                self.sess = self.login_2fa(email)
                self.rsp = requests.post(url, json=body, headers=headers, cookies=cookies)
            elif "Wrong parameters" in con:
                print("Incorrect parameters in POST")
            else:
                print("Successfully logged in")

        rsp = zlib.decompress(self.rsp.content).decode()

        return json.loads(rsp)

    def login_2fa(self, email):
        code = input("Enter the 2fa code: ")
        url = "{}/launcher/hardwareCode/activate?launcherVersion={}".format(
            constants.LAUNCHER_ENDPOINT, constants.LAUNCHER_VERSION
        )

        body = {"email":email, "hwCode":self.hwid, "activateCode":code}
        headers = {
            'User-Agent': 'BSG Launcher {}'.format(constants.LAUNCHER_VERSION),
            'Content-Type': 'application/json' }
        
        rsp = requests.post(url, json=body, headers=headers)
        content = zlib.decompress(rsp.content).decode()
        print("Activation response code: {}".format(rsp.status_code))
        print("Activation response: {}".format(content))
        
        return rsp

    def exchange_access_token(self, access_token, hwid):
        url = "{}/launcher/game/start?launcherVersion={}&branch=live".format(
            constants.PROD_ENDPOINT, constants.LAUNCHER_VERSION
        )
        body = {"version": {"major":constants.GAME_VERSION, "backend":"6"}, "hwCode":hwid}
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'BSG Launcher {}'.format(constants.LAUNCHER_VERSION),
            'Authorization': access_token }
        content = None

        rsp = requests.post(url, json=body, headers=headers)
        try:
            content = zlib.decompress(rsp.content).decode()
        except:
            pass

        if not content:
            print("exchange_access_token failed; {}".format(rsp.status_code))
        elif "errmsg" in content and '"err":0,' not in content:
            print("Error while authorizing: {}".format(content))
        else:
            print("Successfully authorized")
            return json.loads(content)

        print("Unable to complete authorization, exiting")
        print(rsp.status_code)
        print(content)
        exit(-1)