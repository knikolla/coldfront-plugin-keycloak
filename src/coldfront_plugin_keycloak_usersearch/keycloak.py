import requests


class KeycloakClient(object):
    def __init__(self, url, realm, client_id, client_secret):
        self.url = url
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret

        self.session = requests.session()
        self._client_auth()

    def construct_url(self, realm, path):
        return f'{self.url}/admin/realms/{realm}/{path}'

    @property
    def url_base(self):
        return f'{self.url}/admin/realms'

    def auth_endpoint(self, realm):
        return f'{self.url}/realms/{realm}/protocol/openid-connect/auth'

    def token_endpoint(self, realm):
        return f'{self.url}/realms/{realm}/protocol/openid-connect/token'

    def _client_auth(self):
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(self.token_endpoint(self.realm), data=params)
        response.raise_for_status()
        r = response.json()
        if 'access_token' not in r:
            raise ValueError('Keycloak token response did not include access_token')
        headers = {
            'Authorization': 'Bearer ' + r['access_token'],
            'Content-Type': 'application/json'
        }
        self.session.headers.update(headers)
        return r

    def search_username(self, username, realm):
        self._client_auth()
        return self.session.get(self.construct_url(
            realm, f'users?username={username}')).json()

    def search(self, value, realm):
        self._client_auth()
        return self.session.get(self.construct_url(
            realm, f'users?search={value}')).json()
