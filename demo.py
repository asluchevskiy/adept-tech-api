# -*- coding: utf-8 -*-
import logging
from adept_tech_api import AdeptTechApi

INSTANCE = 'demo'
REDIRECT_URL = 'https://localhost/redirect_url'
CLIENT_ID = '__CLIENT_ID__'
CLIENT_SECRET = '__CLIENT_SECRET__',

CODE = '__CODE_FROM_REDIRECT_URL__'
REFRESH_TOKEN = '__REFRESH_TOKEN_FROM_PREVIOUS_AUTH__'
ACCESS_TOKEN = '__ACCESS_TOKEN_FROM_PREVIOUS_AUTH__'

try:
    from local import *
except ImportError:
    pass


def demo_authorization_url():
    api = AdeptTechApi(instance=INSTANCE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URL)
    authorization_url = api.start_oauth()
    print(authorization_url)


def demo_token():
    api = AdeptTechApi(instance=INSTANCE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URL)
    token = api.finish_oauth(code=CODE)
    print(token)


def demo_refresh_token():
    api = AdeptTechApi(instance=INSTANCE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=REDIRECT_URL,
                       access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
    token = api.refresh_token()
    print(token)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    demo_authorization_url()
    # demo_token()
    # demo_refresh_token()
