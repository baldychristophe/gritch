import os
import tempfile

import diskcache


CACHE_DIR = os.path.join(tempfile.gettempdir(), 'gritch-cache')


cache = diskcache.Cache(CACHE_DIR)
