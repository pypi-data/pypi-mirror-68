import boto3
import traceback
import warnings
import base64
import pickle
import numpy as np
import pandas as pd
import sys
import json
import operator
import os
import psutil
import time

from types import ModuleType
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpc.client import ServerProxy

from pympler import asizeof
from botocore.errorfactory import ClientError

from cloudpy.errors import MemoryExceededError

from npc_internal.protocol import Request, Response, ProxyId
from npc_internal.util import get_fullname
from npc_internal.logger import logger
from npc_internal import config


s3 = boto3.client('s3')


class Handler(SimpleXMLRPCRequestHandler):
    def _dispatch(self, method, params):
        try: 
            return self.server.funcs[method](*params)
        except:
            import traceback
            traceback.print_exc()
            raise


class ProxyLibrary(object):

    def __init__(self):
        self.objects = {}
        self.objects_to_id = {}
        self.objects_to_insertion_time = {}

    def store(self, value, proxy_id=None):
        if id(value) in self.objects_to_id:
            return self.objects_to_id[id(value)]

        if proxy_id is None:
            proxy_id = ProxyId.random_id(classname=get_fullname(value.__class__))
        self.objects[proxy_id.pxid] = value

        proc = psutil.Process(os.getpid())
        proc_mem = proc.memory_info().rss
        mem2 = sys.getsizeof(value)

        print('proc mem: %s, getsizeof: %s' % (proc_mem, mem2))

        if 'memory_usage' in dir(value):
            mem = value.memory_usage()
            if not isinstance(mem, int):
                mem = mem.sum()
            print('memory usage via sum(): %s' % mem)
            if mem > config.MAX_MEMORY:
                raise MemoryExceededError()

        self.objects_to_id[id(value)] = proxy_id
        self.objects_to_insertion_time[id(value)] = time.time()

        self.pprint()

        self.maybe_prune()

        return proxy_id

    def pprint(self):
        ids_by_time = list(self.objects_to_insertion_time.keys())
        ids_by_time.sort(key=lambda x: self.objects_to_insertion_time[x])

        print('-' * 40)
        print('\t'.join(['i', 'pxid', 't', 'getsizeof', 'memory_usage().sum', 'nbytes']))
        for idx, i in enumerate(ids_by_time):
            proxy_id = self.objects_to_id[i]
            t = self.objects_to_insertion_time[i]
            obj = self.objects[proxy_id.pxid]
            mem = sys.getsizeof(obj)
            mem2 = -1
            mem3 = -1
            if 'memory_usage' in dir(obj):
                mem2 = obj.memory_usage()
                if not isinstance(mem2, int):
                    mem2 = mem2.sum()

            if 'nbytes' in dir(obj):
                try:
                    mem3 = int(obj.nbytes)
                except:
                    pass

            print('%s\t%s\t%d\t%.1f MB\t%.1f MB\t%.1f MB' % (idx, proxy_id.pxid, t, mem/1e6, mem2/1e6, mem3/1e6))
        print('-' * 40)

    def maybe_prune(self):
        total_usage = 0

        ids_by_time = list(self.objects_to_insertion_time.keys())
        ids_by_time.sort(key=lambda x: self.objects_to_insertion_time[x])

        for i in ids_by_time:
            proxy_id = self.objects_to_id[i]
            obj = self.objects[proxy_id.pxid]
            total_usage += self.estimate_mem(obj)

        need_to_prune = total_usage - config.MAX_LIBRARY_MEMORY
        for i in ids_by_time:
            print('need to prune: %.1f MB' % (need_to_prune / float(1e6)))
            if need_to_prune < 0:
                break
            proxy_id = self.objects_to_id[i]
            obj = self.objects[proxy_id.pxid]
            mem = self.estimate_mem(obj)
            self.evict(obj)
            need_to_prune -= mem

    def evict(self, obj):
        proxy_id = self.objects_to_id[id(obj)]
        print('evicting', proxy_id.pxid)
        del self.objects_to_id[id(obj)]
        del self.objects_to_insertion_time[id(obj)]
        del self.objects[proxy_id.pxid]

    def estimate_mem(self, obj):
        mem = None
        if 'memory_usage' in dir(obj):
            try:
                mem = obj.memory_usage()
                if not isinstance(mem, int):
                    mem = mem.sum()
            except:
                pass
        if 'nbytes' in dir(obj):
            try:
                mem = int(obj.nbytes)
            except:
                pass
        if not mem:
            mem = sys.getsizeof(obj)
        return mem
        

    def get(self, proxy_id):
        obj = self.objects.get(proxy_id.pxid)

        cloudpy_path = None
        if obj is None and proxy_id.can_import:
            cloudpy_path = proxy_id.path.replace('cloudpy.', 'cloudpy_')
            # import pdb ; pdb.set_trace()
            # module_name = use_path.split('.')[1]  # cloudpy.numpy -> numpy
            name = cloudpy_path.partition('.')[0]
            module_name = {
                'cloudpy_numpy': 'numpy',
                'cloudpy_pandas': 'pandas',
            }[name]
            obj = __import__(module_name)
            self.store(obj, proxy_id)

        if proxy_id.path:
            # TODO: refactor so modules use same path semantics as objects
            if proxy_id.can_import:
                part = cloudpy_path.partition('.')[2]
                if part:
                    obj = operator.attrgetter(part)(obj)
            else:
                logger.debug('Doing path lookup for proxyid: %s' % (proxy_id))
                obj = operator.attrgetter(proxy_id.path)(obj)

        return obj


class CloudArrayServer(object):

    should_proxy_types = {get_fullname(x): x for x in [
        pd.Series,
        pd.DataFrame,
        pd.Panel,
        pd.Int64Index,
        pd.core.indexing._iLocIndexer,
        pd.core.groupby.DataFrameGroupBy,
        pd.core.internals.BlockManager,
        pd.core.indexes.multi.MultiIndex,
        pd.core.indexes.base.Index,

        np.ndarray,
        np.flatiter,
        np.nditer,
        np.core.multiarray.flagsobj,

        ModuleType,
    ]}

    def __init__(self, host, port):
        self.spec = (host, port)
        self.url = 'http://%s:%s' % self.spec
        self.server = SimpleXMLRPCServer(self.spec, Handler, logRequests=False)
        self.data_bucket = config.DATA_BUCKET

        self.server.register_function(self.stop, 'stop')
        self.server.register_function(self.pull, 'pull')
        self.server.register_function(self.proxy, 'proxy')
        self.server.register_function(self.init, 'init')
        self.server.register_function(self.save, 'save')
        self.server.register_function(self.load, 'load')
        self.server.register_function(self.has_file, 'has_file')
        self.server.register_function(self.upload_url, 'upload_url')
        self.server.register_function(self.from_file, 'from_file')

        self.stopped = False
        self.lib = ProxyLibrary()

    def serve(self):
        logger.info('== serving on: %s ==', self.spec)
        while not self.stopped:
            self.server.handle_request()
        self.server.server_close()

    def force_stop(self):
        url = 'http://%s:%s' % self.spec
        with ServerProxy(url) as client:
            client.stop()

    def stop(self):
        self.stopped = True
        return 'ok'

    def pull(self, req_ser):
        req = Request.deserialize(req_ser, self.lib)
        proxy_id = req.proxy_id
        obj = self.lib.get(proxy_id)
        resp = Response(obj, [], self.lib)
        return resp.serialize()

    def init(self, req_ser):
        req = Request.deserialize(req_ser, self.lib)
        classname = req.meta['class']
        clazz = self.should_proxy_types[classname]
        obj = clazz(*req.args, **req.kwargs)
        resp = Response(obj, self.should_proxy_types, self.lib)
        return resp.proxy_id.serialize()

    def save(self, proxy_id_ser, apikey, name):
        raise Exception('saving only available for beta API keys, email hello@cloudpy.io to get one')

        proxy_id = ProxyId.deserialize(proxy_id_ser)
        obj = self.lib.get(proxy_id)

        if obj is None:
            return 'not found'

        ser_data = None

        if proxy_id.classname == 'pandas.core.frame.DataFrame':
            filename = '%s-%s.pkl' % (apikey, name)
            filename = filename.replace('/', '__')
            path = '/tmp/%s' % filename
            print('save to:', path)
            obj.to_pickle(path)
            with open(path, 'rb') as f:
                key = 'user_data/%s' % filename
                print('saving %s/%s to s3' % (self.data_bucket, key))
                resp = s3.put_object(Body=f, Bucket=self.data_bucket, Key=key)
                print('s3 resp', resp)
            return 'ok'
        
        return "can't save"

    def load(self, apikey, name):
        if apikey not in  ['sandbox', 'localhost']:
            raise Exception('%s is unavailable for loading' % apikey)
        if name != 'public/MSFT':
            raise Exception('%s is unavailable for loading' % name)

        filename = '%s-%s.pkl' % (apikey, name)
        filename = filename.replace('/', '__')
        key = 'user_data/%s' % filename
        path = '/tmp/%s' % filename
        with open(path, 'wb') as data:
            s3.download_fileobj(self.data_bucket, key, data)
        obj = pd.read_pickle(path)
        return Response(obj, self.should_proxy_types, self.lib).serialize()
        # print('read obj:', obj)
        # proxy_id = self.lib.store(obj)
        # print('got proxy_id', proxy_id)
        # return proxy_id.pxid

    def proxy(self, req_ser):
        req = Request.deserialize(req_ser, self.lib)
        proxy_id = req.proxy_id
        obj = self.lib.get(proxy_id)

        logger.debug('--> Proxy: %s', req.field_name)
        logger.debug('    args: %s', req.args)
        logger.debug('    kwargs: %s', req.kwargs)
        logger.debug('    obj: %s', type(obj))

        if req.call_as not in ['method', 'attr', 'classmethod']:
            raise Exception('unexpected: %s' % req.call_as)

        try:
            if req.call_as == 'method':
                if req.field_name is None:
                    method = obj
                else:
                    method = operator.attrgetter(req.field_name)(obj)
                rval = method(*req.args, **req.kwargs)
            elif req.call_as == 'classmethod':
                clazz = req.args[0]
                args = req.args[1:]
                cls_method = getattr(clazz, req.field_name)
                rval = cls_method(*args, **req.kwargs)
            elif req.call_as == 'attr':
                field = operator.attrgetter(req.field_name)(obj)
                rval = field
        except Exception as e:
            logger.info('Returning exception %s', e)
            logger.debug('Stack trace: %s', ''.join(traceback.format_exception(
                None, e, e.__traceback__)))
            rval = e

        resp = Response(rval, self.should_proxy_types, self.lib)
        ser = resp.serialize()
        size = asizeof.asizeof(ser)
        logger.debug('Serialized response size is: %s bytes', size)

        if size > 1000:
            logger.debug('Large response with size: %s, class: %s' % (size, get_fullname(rval.__class__)))

        return ser

    def _key_for_hash(self, file_hash, content_type):
        ext = content_type.split('/')[1]
        return 'files/%s.%s' % (file_hash, ext)

    def has_file(self, file_hash, content_type):
        key = self._key_for_hash(file_hash, content_type)
        try:
            s3.head_object(Bucket=self.data_bucket, Key=key)
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise e
        return True

    def upload_url(self, file_hash, content_type):
        key = self._key_for_hash(file_hash, content_type)
        url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': self.data_bucket, 'Key': key, 'ContentType': content_type})
        return url

    def from_file(self, file_hash, content_type, req_ser):
        # TODO: re-use same dataframe in read-only or copy-on-write mode
        req = Request.deserialize(req_ser, self.lib)
        key = self._key_for_hash(file_hash, content_type)
        obj = s3.get_object(Bucket=self.data_bucket, Key=key)
        fn = {
            'text/csv': pd.read_csv,
        }[content_type]
        kwargs = req.kwargs
        rval = fn(obj['Body'], **kwargs)
        resp = Response(rval, self.should_proxy_types, self.lib)
        ser = resp.serialize()
        return ser


if __name__ == '__main__':
    host = 'localhost'
    port = 9090

    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    server = CloudArrayServer(host, port)
    server.serve()
