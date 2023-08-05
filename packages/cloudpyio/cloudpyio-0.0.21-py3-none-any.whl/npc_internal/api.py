import os
import secrets
import time

import requests

from npc_internal.logger import logger


API_HOST = os.environ.get('API_HOST', 'https://cloudpy-server.herokuapp.com')

cache = {}
_apikey = None


def random_apikey():
    return 'sandbox'


def set_apikey(set_apikey):
    global _apikey
    logger.debug('have: %s, set: %s' % (_apikey, set_apikey))
    if _apikey and set_apikey != _apikey:
        raise Exception('already set api key')
    _apikey = set_apikey


def get_apikey():
    global _apikey
    if not _apikey:
        set_apikey(random_apikey())
    return _apikey


def get_server_url():
    apikey = get_apikey()

    cached_value = cache.get(apikey)
    if cached_value:
        return cached_value

    print('cloudpy: connecting to the cloud')
    url = '%s/api/instances/init' % API_HOST
    params = {'apikey': apikey}
    logger.debug('params', params)
    resp = requests.post(url, data=params)
    logger.debug(resp)
    data = resp.json()
    for i in range(100):
        host = data.get('host')
        status = data.get('status')
        if host and status == 'running':
            break
        print('cloudpy: initializing, host=%s, status=%s' % (host, status))
        host = None
        time.sleep(2)
    if not host:
        raise Exception('unable to get a cloudpy host')
    url = 'http://%s:9090' % host
    logger.debug('got url --> %s' % url)
    cache[apikey] = url
    return url
