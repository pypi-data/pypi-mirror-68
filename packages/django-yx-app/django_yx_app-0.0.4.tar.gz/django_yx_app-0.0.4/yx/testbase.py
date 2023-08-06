import json
import os
import unittest

from django.conf import settings
from django.test import Client

TEST_RESULTS_DIR = os.path.join(settings.BASE_DIR, 'test_results')


class HttpException(BaseException):
    def __init__(self, rsp):
        super(HttpException, self).__init__()
        self.rsp = rsp

    def __str__(self):
        return '<Response: %d>' % self.rsp.status_code


class TestBase(unittest.TestCase):
    """
    Base class for django unit test
    forbid copy of database
    """

    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)
        self._client = Client()  # use django client

    def _call_http_method(self, method, path, data=None):
        data = data or {}
        self._save_url(data, path, method, '-request')

        jsonstring = json.dumps(data)
        client_method = getattr(self._client, method.lower())
        rsp = client_method(path, data=jsonstring, content_type='application/json')
        if rsp.status_code != 200:
            raise HttpException(rsp)
        self._save_url(rsp.content, path, method)
        return rsp

    def _save_url(self, s, path, method, suffix='-response'):
        if isinstance(s, dict):
            s = json.dumps(s)

        test_root = TEST_RESULTS_DIR
        fdir = test_root + '/' + path  # os.path.join(test_root, path)
        if not os.path.isdir(fdir):
            os.makedirs(fdir)
        filepath = os.path.join(fdir, method + suffix + '.json')
        open(filepath, 'wb').write(s)

    def get(self, path, data=None):
        data = data or {}
        self._save_url(data, path, 'get', suffix='-request')
        rsp = self._client.get(path, data)  ####use origin
        if rsp.status_code != 200:
            raise HttpException(rsp)
        self._save_url(rsp.content, path, 'get', suffix='-response')
        return rsp

    def post(self, url, data=None, data_format='json'):
        data_format = data_format.lower()
        if data_format == 'json':
            return self._call_http_method(method='post', path=url, data=data)
        # multiform
        self._save_url(data, url, 'post', suffix='-request')
        rsp = self._client.post(url, data)
        if rsp.status_code != 200:
            raise HttpException(rsp)
        self._save_url(rsp.content, url, 'post')
        return rsp

    def put(self, url, data=None):
        return self._call_http_method(method='put', path=url, data=data)

    def patch(self, url, data=None):
        return self._call_http_method(method='patch', path=url, data=data)

    def delete(self, url, data=None):
        return self._call_http_method(method='delete', path=url, data=data)
