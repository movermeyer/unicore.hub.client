import os
import json
from urllib import urlencode
from urlparse import urljoin, urlparse, urlunparse

import requests
from requests.auth import HTTPBasicAuth

from unicore.hub.client.utils import client_from_config


class ClientException(Exception):
    pass


class BaseClient(object):

    def __init__(self, **settings):
        self.settings = settings
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(
            settings['app_id'],
            settings['app_password'])
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.host = settings['host']

    def _make_url(self, path, use_https=False):
        path = os.path.join(getattr(self, 'base_path', ''), path)
        host = self.host

        if use_https and not self.host.startswith('https'):
            parts = urlparse(self.host)
            host = urlunparse(('https', ) + parts[1:])

        return urljoin(host, path)

    def _request(self, method, path, *args, **kwargs):
        return self._request_no_parse(method, path, *args, **kwargs).json()

    def _request_no_parse(self, method, path, *args, **kwargs):
        kwargs = kwargs.copy()
        use_https = kwargs.pop('use_https', False)
        url = self._make_url(path, use_https=use_https)
        resp = self.session.request(method, url, *args, **kwargs)

        if resp.status_code not in (200, 201, 204):
            raise ClientException('HTTP %s: %s' %
                                  (resp.status_code, resp.content))

        return resp

    def get(self, path, *args, **kwargs):
        return self._request('get', path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        kwargs['data'] = json.dumps(kwargs['data'])
        return self._request('post', path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        kwargs['data'] = json.dumps(kwargs['data'])
        return self._request('put', path, *args, **kwargs)

    @classmethod
    def from_config(cls, config, **kwargs):
        return client_from_config(cls, config, **kwargs)


class UserClient(BaseClient):
    base_path = '/users'

    def __init__(self, **settings):
        super(UserClient, self).__init__(**settings)
        self.login_callback_url = settings.get('login_callback_url', None)

    def get_app_data(self, user_id):
        return self.get('%s' % user_id)

    def save_app_data(self, user_id, app_data):
        return self.post('%s' % user_id, data=app_data)

    def _get_login_callback_url(self, login_callback_url=None):
        login_callback_url = login_callback_url or self.login_callback_url

        if not login_callback_url:
            raise ValueError('no login_callback_url provided')

        # check that url is absolute
        parts = urlparse(login_callback_url)
        if not (parts.scheme and parts.netloc):
            raise ValueError('login_callback_url must be absolute')

        return login_callback_url

    def get_login_redirect_url(self, login_callback_url=None, locale=None):
        params = {'service': self._get_login_callback_url(login_callback_url)}
        if locale:
            params['_LOCALE_'] = locale

        use_https = self.settings.get('redirect_to_https', True)
        return self._make_url(
            '/sso/login?%s' % urlencode(params), use_https=use_https)

    def get_user(self, ticket, login_callback_url=None):
        params = {
            'service': self._get_login_callback_url(login_callback_url),
            'ticket': ticket}
        resp = self._request_no_parse('get', '/sso/validate', params=params)

        if resp.content.startswith('no\n'):
            raise ClientException('ticket with login_callback_url is invalid')

        return resp.json()
