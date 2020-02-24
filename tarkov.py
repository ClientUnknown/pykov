from pykov import auth
from pykov import hwid
from pykov import constants
import requests
import json
import zlib

class Tarkov:
    def __init__(self, email, password):
        self.req_counter = 0    # Keep a counter for number of requests made

        constants.check_launcher_version()  # Update launcher version if necessary
        constants.check_game_version()  # Update game version if necessary

        # Retrieve a hwid to use for our connection, attempt to login to EFT
        # servers, generate a session, and then select the profile to be used
        # for all REST queries
        self.hwid = hwid.generate_hwid()
        self.auth = auth.Auth(self.hwid)
        self.user = self.auth.login(email, password)
        self.session = self.auth.exchange_access_token(self.user['data']['access_token'],self.hwid)
        self.session_id = self.session['data']['session']
        self.profile = self.select_profile()
        print("Tarkov connection has been established") # If we get this far, we're in

    # Send a request to the server to keep us connected
    # Disconnects will happen after 30 seconds of inactivity
    def keep_alive(self):
        url = "{}/client/game/keepalive".format(constants.PROD_ENDPOINT)
        body = {}
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'BSG Launcher {}'.format(constants.LAUNCHER_VERSION) }
        
        rsp = requests.post(url, json=body, headers=headers)

        if rsp.status_code == 200:
            print("Connection refreshed")
            return True
        else:
            print("Unable to keep connection alive; error: {}".format(rsp.status_code))
            return False

    # Returns a dictionary of profiles
    def get_profiles(self):
        url = "{}/client/game/profile/list".format(constants.PROD_ENDPOINT)
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)
        
        if not content:
            print("get_profile request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not get profiles list; error: {}".format(content))
        else:
            return json.loads(content)

        return None

    # Selects our profile, returning a dictionary with various profile information
    # This profile will be used for all queries in the session
    def select_profile(self):
        profiles = self.get_profiles()
        for profile in profiles['data']:
            if profile['Info']['Side'] != 'Savage':
                self.profile = profile
        if not self.profile:
            print("Could not find profile")
            return None

        url = "{}/client/game/profile/select".format(constants.PROD_ENDPOINT)
        body = {"uid": self.profile['_id'].rstrip()}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)
        
        if not content:
            print("select_profile request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not select profile; error: {}".format(content))
        else:
            return json.loads(content)

        return None

    # Returns a dictionary with the currently selected profile's friends
    def get_friends(self):
        url = "{}/client/friend/list".format(constants.PROD_ENDPOINT)
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)
        
        if not content:
            print("get_friends request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not get friends list; error: {}".format(content))
        else:
            return json.loads(content)

        return None

    # Returns a dictionary of all traders
    def get_traders(self):
        url = "{}/client/trading/api/getTradersList".format(constants.TRADING_ENDPOINT)
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)

        if not content:
            print("get_traders request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not get traders list; error: {}".format(content))
        else:
            return json.loads(content)

        return None

    # Returns a dictionary with a specific trader's information
    def select_trader(self, trader_name):
        trader_id = self.get_trader_id(trader_name)
        if not trader_id:
            return None

        url = "{}/client/trading/api/getTrader/{}".format(
            constants.TRADING_ENDPOINT, trader_id
        )
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)

        if not content:
            print("select_trader request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not select trader; error: {}".format(content))
        else:
            return json.loads(content)
        
        return None

    # Returns a dictionary with all items that a trader sells based on your profile
    def get_trader_items(self, trader_name):
        trader_id = self.get_trader_id(trader_name)
        if not trader_id:
            return None

        url = "{}/client/trading/api/getTraderAssort/{}".format(
            constants.TRADING_ENDPOINT, trader_id
        )
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)

        if not content:
            print("get_trader_items request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not get trader's items; error: {}".format(content))
        else:
            return json.loads(content)

        return None

    # Gets the schema ID for a trader based on their English name
    def get_trader_id(self, trader_name):
        locale = self.get_i18n_english()
        traders = self.get_traders()

        for key in locale['data']['trading']:
            if locale['data']['trading'][key]['Nickname'] == trader_name:
                return key

        print("Unable to find requested trader {}".format(trader_name))
        return None

    # Returns a dictionary with all the items in the game
    def get_items(self):
        url = "{}/client/items".format(constants.PROD_ENDPOINT)
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)

        if not content:
            print("get_items request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not fetch items list; error: {}".format(content))
        else:
            return json.loads(content)
        
        return None

    # Returns a dictionary with the English translation table
    def get_i18n_english(self):
        url = "{}/client/locale/en".format(constants.PROD_ENDPOINT)
        body = {}
        headers = self.__get_headers_client()

        rsp = requests.post(url, json=body, headers=headers)
        content = self.__decompress_json_request(rsp.content)

        if not content:
            print("get_i18n_english request failed: {}".format(rsp.status_code))
        elif rsp.status_code != 200:
            print("Could not get translation table; error: {}".format(content))
        else:
            return json.loads(content)

        return None

    def __decompress_json_request(self, content):
        try:
            content = zlib.decompress(content).decode()
        except:
            return None
        return content

    def __get_headers_client(self):
        self.req_counter += 1
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'UnityPlayer/{} (UnityWebRequest/1.0, libcurl/7.52.0-DEV)'.format(constants.UNITY_VERSION),
            'App-Version': 'EFT Client {}'.format(constants.GAME_VERSION),
            'X-Unity-Version': constants.UNITY_VERSION,
            'Cookie': 'PHPSESSID={}'.format(self.session_id),
            'GClient-RequestId': str(self.req_counter)
        }
        return headers