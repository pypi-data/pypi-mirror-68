import os
import requests
import psutil

from xmlrpc.client import ServerProxy

from npc_internal import api
from npc_internal.protocol import Response
from npc_internal.proxy_objects import get_proxy_id
from npc_internal.proxy import get_factory_singleton


def init(apikey=None):
    print('init')
    api.set_apikey(apikey)


def memory_info():
    proc = psutil.Process(os.getpid())
    return proc.memory_info()


def save(obj, name):
    proxy_id = get_proxy_id(obj)
    print('save proxy_id', proxy_id)
    with ServerProxy(api.get_server_url(), allow_none=True) as server:
        server.save(proxy_id.serialize(), api.get_apikey(), name)


def load(name):
    with ServerProxy(api.get_server_url(), allow_none=True) as server:
        resp_ser = server.load(api.get_apikey(), name)
        resp = Response.deserialize(resp_ser)
        return resp.unpack(get_factory_singleton())
