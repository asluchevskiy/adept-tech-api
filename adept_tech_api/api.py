# -*- coding: utf-8 -*-
import re

import requests
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode, urljoin

AUTH_URL = 'https://api.adept.tech/v1/authorize?instance=__INSTANCE__'
TOKEN_URL = 'https://api.adept.tech/v1/access_token?instance=__INSTANCE__'
USER_URL = 'https://api.adept.tech/v1/me?instance=__INSTANCE__'
BASE_URL = 'https://api.adept.tech/v1/api'


class AdeptTechApi:
    _client_id = None
    _client_secret = None
    _redirect_url = None
    _refresh_token = None
    _access_token = None

    _scopes = None
    _instance = None

    _base_url = BASE_URL
    _auth_url = AUTH_URL
    _token_url = TOKEN_URL
    _user_url = USER_URL

    def __init__(self, instance, client_id, client_secret, redirect_url, scopes=None,
                 refresh_token=None, access_token=None):

        if type(instance) is not str or not re.match('^[a-zA-Z]+[a-zA-Z0-9-]+[a-zA-Z0-9]+$', instance):
            raise ValueError('invalid instance name: %s' % instance)
        self._instance = instance

        if scopes is None:
            scopes = []
        self._scopes = scopes

        self._auth_url = self._auth_url.replace('__INSTANCE__', instance)
        self._token_url = self._token_url.replace('__INSTANCE__', instance)
        self._user_url = self._user_url.replace('__INSTANCE__', instance)

        self._client_id = client_id
        self._client_secret = client_secret

        self._redirect_url = redirect_url
        self._refresh_token = refresh_token
        self._access_token = access_token

        self._provider = OAuth2Session(client_id=self._client_id, client_secret=self._client_secret,
                                       redirect_uri=self._redirect_url)

    @property
    def scopes(self):
        return self._scopes

    def start_oauth(self, state=None):
        authorization_url, provider_state = self._provider.create_authorization_url(
            url=self._auth_url,
            scope=' '.join(self._scopes),
            state=state if state is not None else self._provider.state,
        )
        return authorization_url

    def finish_oauth(self, code):
        token = self._provider.fetch_token(self._token_url, authorization_response=f'?code={code}')
        self._access_token = token.get('access_token')
        self._refresh_token = token.get('refresh_token')
        return token

    def refresh_token(self):
        new_token = self._provider.refresh_token(self._token_url, refresh_token=self._refresh_token)
        self._access_token = new_token.get('access_token')
        self._refresh_token = new_token.get('refresh_token')
        return new_token

    def call(self, endpoint, method='GET', params=None):
        if params is None:
            params = {}
        params['instance'] = self._instance
        headers = {
            'Authorization': self._access_token
        }
        url = urljoin(self._base_url + '/', endpoint)
        resp = requests.request(method=method, url=url, params=params, headers=headers)
        return resp.json()
