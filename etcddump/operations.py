from urlparse import urlparse
import etcd
import json
import sys


class BaseOperations(object):

    def __init__(self, url='http://localhost:4001'):
        self.get_client(url)


    def get_client(self, url, ca_cert=None, cert=None):
        parsed = urlparse(url)
        (h, p) = parsed.netloc.split(':')
        self.client = etcd.Client(host=h, port=int(p), protocol=parsed.scheme, allow_reconnect=False, ca_cert=ca_cert, cert=cert)

    def entry_from_result(self, entry):
        return {
            'key': entry.key,
            'value': entry.value,
            'ttl': entry.ttl,
            'dir': entry.dir,
            'index': entry.modifiedIndex
        }


class Dumper(BaseOperations):


    def dump(self, filename=None):
        data = self.client.read('/', recursive=True)
        d = {}
        for entry in data.children:
            d[entry.modifiedIndex] = self.entry_from_result(entry)

        indexes = sorted(d.keys())
        dumplist = []
        for idx in indexes:
            dumplist.append(d[idx])

        if filename:
            with open(filename, 'w') as f:
                json.dump(dumplist,f)
        else:
            print(json.dumps(dumplist))

class Restorer(BaseOperations):
    def fake_entry(self):
        return {
            'key': '/_etcd_dumper/bogus',
            'value': 'bogus',
            'ttl': 1,
            'dir': False
        }

    def restore(self, filename=None, preserve_indexes=False):
        if filename:
            with open(filename, 'rb') as f:
                data = json.load(f)
        else:
            with sys.stdin as f:
                data = json.load(f)

        lastidx = 0

        for entry in data:
            if preserve_indexes:
                self.fillin(entry['index'], lastidx)

            r = self.write(entry)
            lastidx = r.modifiedIndex

    def fillin(self, idx, lastidx):
        while (idx < (lastidx - 1)):
            r = self.write(fake_entry)
            idx = r.modifiedIndex
        return idx

    def write(self, entry):
        return self.client.write(entry['key'], entry['value'], ttl = entry['ttl'], dir = entry['dir'])
