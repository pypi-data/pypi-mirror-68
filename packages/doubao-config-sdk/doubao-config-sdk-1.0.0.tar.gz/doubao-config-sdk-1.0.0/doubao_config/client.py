import requests
import os
from .errors import RequestException


class Client(object):
    __token = None

    def __init__(self, host, username, password):
        self.host = host if host.startswith('http') else 'http://%s' % host
        if not self.host.endswith('/'):
            self.host = self.host + '/'
        self.username = username
        self.password = password
        self.session = requests.Session()

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, v):
        self.__token = v

    def _request(self, endpoint, method='POST', params=None, data=None, headers=None, json=None):
        url = self.host + endpoint
        rep = self.session.request(method, url, params=params, data=data, headers=headers, json=json)
        if rep.status_code != 200:
            raise RequestException('http code error: {} {}'.format(rep.status_code, rep.text))
        res = rep.json()
        if 'success' in res:
            if res['success'] is not True:
                raise RequestException('not success: {}'.format(res["msg"]))
            return res['data']
        else:
            return res

    def request(self, endpoint, method='POST', params=None, data=None, headers=None, json=None):
        if not self.token:
            self.refresh_token()

        for i in range(2):
            try:
                _headers = {"token": self.token, **headers} if headers else {"token": self.token}
                return self._request(endpoint, method=method, params=params, data=data, headers=_headers, json=json)
            except RequestException as e:
                if i > 0:
                    raise e
                self.refresh_token()
            except Exception as e:
                raise e

    def refresh_token(self):
        result = self._request('api/login', method='GET', params={'userName': self.username, 'passWord': self.password})
        self.token = result['token']
    
    def get_config(self, application, profile):
        result = self.request('api/config', method='POST', json={'application': application, 'profile': profile})
        return result['propertySources'][0]['source'] if result['propertySources'] else {}
    
    @classmethod
    def set_env(cls, host, username, password, application, profile):
        client = cls(host, username, password)
        configs = client.get_config(application, profile)
        for k, v in configs.items():
            os.environ[k] = v
