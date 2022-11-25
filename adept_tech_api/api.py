# -*- coding: utf-8 -*-
import re
from authlib.integrations.requests_client import OAuth2Session

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

    def __init__(self, instance, client_id, client_secret, redirect_url, scopes=None,
                 refresh_token=None, access_token=None):

        if type(instance) is not str or not re.match('^[a-zA-Z]+[a-zA-Z0-9-]+[a-zA-Z0-9]+$', instance):
            raise ValueError('invalid instance name: %s' % instance)
        self._instance = instance

        if scopes is None:
            scopes = []
        self._scopes = scopes

        self._auth_url = AUTH_URL.replace('__INSTANCE__', instance)
        self._token_url = TOKEN_URL.replace('__INSTANCE__', instance)
        self._user_url = USER_URL.replace('__INSTANCE__', instance)

        self._client_id = client_id
        self._client_secret = client_secret

        self._redirect_url = redirect_url
        self._refresh_token = refresh_token
        self._access_token = access_token

    def start_oauth(self, state=None):
        # $provider = new \League\OAuth2\Client\Provider\GenericProvider([
        #     'clientId'                => $this->client_id,
        #     'clientSecret'            => $this->client_secret,
        #     'redirectUri'             => $this->redirect_url,
        #     'urlAuthorize'            => str_replace('__INSTANCE__', $this->instance, self::auth_url),
        #     'urlAccessToken'          => str_replace('__INSTANCE__', $this->instance, self::token_url),
        #     'urlResourceOwnerDetails' => str_replace('__INSTANCE__', $this->instance, self::user_url),
        # ]);
        #
        # header('Location: '.$provider->getAuthorizationUrl([
        #         'scope' => implode(' ', $this->scopes),
        #         'state' => $state !== null ? $state : $provider->getState(),
        #     ]));
        provider = OAuth2Session(client_id=self._client_id, client_secret=self._client_secret,
                                 redirect_uri=self._redirect_url)
        authorization_url, provider_state = provider.create_authorization_url(
            url=self._auth_url,
            scope=' '.join(self._scopes),
            state=state if state is not None else provider.state,
        )
        return authorization_url

    def finish_oauth(self, code):
        # // Try to get an access token using the authorization code grant.
        # $token               = $provider->getAccessToken('authorization_code', [
        #     'code' => $code,
        # ]);
        # $this->access_token  = $token->getToken();
        # $this->refresh_token = $token->getRefreshToken();
        #
        # return $token;
        provider = OAuth2Session(client_id=self._client_id, client_secret=self._client_secret,
                                 redirect_uri=self._redirect_url)
        token = provider.fetch_token(self._token_url, authorization_response=f'?code={code}')
        self._access_token = token.get('access_token')
        self._refresh_token = token.get('refresh_token')
        return token

    def refresh_token(self):
        # $provider = new \League\OAuth2\Client\Provider\GenericProvider([
        #     'clientId'                => $this->client_id,
        #     'clientSecret'            => $this->client_secret,
        #     'redirectUri'             => $this->redirect_url,
        #     'urlAuthorize'            => str_replace('__INSTANCE__', $this->instance, self::auth_url),
        #     'urlAccessToken'          => str_replace('__INSTANCE__', $this->instance, self::token_url),
        #     'urlResourceOwnerDetails' => str_replace('__INSTANCE__', $this->instance, self::user_url),
        # ]);
        #
        # // Try to get an access token using the authorization code grant.
        # return $provider->getAccessToken('refresh_token', [
        #     'refresh_token' => $this->refresh_token(),
        # ]);
        # todo: in some reason got an error
        #  unsupported_grant_type: The authorization grant type is not supported by the authorization server.
        provider = OAuth2Session(client_id=self._client_id, client_secret=self._client_secret,
                                 redirect_uri=self._redirect_url)
        new_token = provider.refresh_token(self._token_url, refresh_token=self._refresh_token)
        self._access_token = new_token.get('access_token')
        self._refresh_token = new_token.get('refresh_token')
        return new_token

    def call(self, endpoint, method='GET', params=None):
        # todo: finish call method
        # $params['instance'] = $this->instance;
        # $q = [];
        # foreach($params as $k => $v) {
        #     $q[] = $k.'='.urlencode($v);
        # }
        # $endpoint = self::base_url.'/'.$endpoint.'?'.implode('&', $q);
        #
        # $client = new \GuzzleHttp\Client();
        # $response = $client->request($method, $endpoint, [
        #         'headers' => [
        #             'Authorization' => $this->access_token,
        #         ],
        #     ]
        # );
        #
        # return json_decode($response->getBody()->getContents());
        if params is None:
            params = {}
        params['instance'] = self._instance
        q = {}
