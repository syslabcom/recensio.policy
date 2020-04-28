import os
import threading

import memcache
from plone.memoize.interfaces import ICacheChooser
from plone.memoize.ram import MemcacheAdapter
from zope.interface import directlyProvides

thread_local = threading.local()


def choose_cache(fun_name):
    global servers

    client = getattr(thread_local, "client", None)
    if client is None:
        servers = os.environ.get("MEMCACHE_SERVER", "195.62.125.219:11211").split(",")
        client = thread_local.client = memcache.Client(servers, debug=1)

    return MemcacheAdapter(client)


directlyProvides(choose_cache, ICacheChooser)
