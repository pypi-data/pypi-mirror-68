from .info import sys_info, citation_text
from .misc import resize_dask_cache

#: dask.cache.Cache, optional : A dask cache for opportunistic caching
#: use :func:`~.resize_dask_cache` to actually register and resize.
dask_cache = None
