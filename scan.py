import requests
from pprint import pprint
from robin_stocks.helper import update_session, request_post,SESSION
from robin_stocks.robinhood import get_all_watchlists
import json
import os
import pickle
import random



class Scan:
    def __init__(self, token=None):
        self.token = token if token else self.return_token()
        self.header = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-Robinhood-API-Version': '1.431.4',
            'Authorization': 'Bearer ' + f'{self.token}',
            'X-Minerva-API-Version': '1.100.0',
            'X-Phoenix-API-Version': '0.0.3',
            'X-Nummus-API-Version': '1.41.11',
            'Accept-Encoding': 'gzip,deflate',
            'X-Midlands-API-Version': '1.66.64',

            'X-Hyper-Ex': 'enabled',            
        }

        
    def return_token(self,name=""):
        """Get the token from the pickle file"""
        home_dir = os.path.expanduser("~")
        data_dir = os.path.join(home_dir, ".tokens")
        creds_file = "robinhood" + name + ".pickle"
        pickle_path = os.path.join(data_dir, creds_file)
        with open(pickle_path, 'rb') as f:
            pickle_data = pickle.load(f)
            self.access_token = pickle_data['access_token']
        return self.token
      
    
    @property
    def emoji(self):
        """
        this is a property that returns a random emoji, TODO: remove this
        """
        return_emoji = [
        "\U0001F680",
        "\U0001F603",
        "\U0001F6D1",
        "\U00002705",
        "\U0000274E",
        "\U0001F4B0",
        "\U0001F4B1",
        "\U0001F44E",
        "\U0001F44D",
        "\U0001F426",
        "\U0001F4E9",
        "\U0001F33B",
        "\U0001F340",
        "\U0001F339"


        ]
        random.shuffle(return_emoji)
        return random.choice(return_emoji)
    
    def create_watchlist(self,name: str) -> str:
        data = {
            "display_name" : name,
            "icon_emoji" : self.emoji,
        }
        try:
            SESSION.headers.update(self.header)
            requested_info = SESSION.post('https://api.robinhood.com/midlands/lists/', data=json.dumps(data))
            requested_info.raise_for_status()
        except requests.exceptions.HTTPError as message:
            print(message)
        return requested_info
    
    
    def delete_watchlist(self,name: str) -> str:
        all_watchlists = get_all_watchlists()
        if name is None:
            return "No watchlist name provided,its required"
        watchist_name = [name].pop()
        watchlist_id = None
        for wl in all_watchlists['results']:
            if wl['display_name'] in watchist_name:
                watchlist_id = wl['id']
                break
        
            
        try:
            SESSION.headers.update(self.header)
            if watchlist_id is None:
                return "No watchlist found with that name"
            requested_info = SESSION.delete(f'https://api.robinhood.com/midlands/lists/{watchlist_id}/')
            requested_info.raise_for_status()
        except requests.exceptions.HTTPError as message:
            print(message)
        return requested_info
    
    
    
    @classmethod
    def indicators(cls,indicator: str, symbol: str) -> str:
        ...


        
        
