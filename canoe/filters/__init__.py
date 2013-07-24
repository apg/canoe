"""Chisels

Chisels are just functions that take a line and a buffer keep an eye out
for something interesting. If they don't find anything, they should just
return `(None, None)`

If, however, they do find something worth looking at, they continue down
the chain of filters until they exhaust them, or stop being interested
in them. 

Chisels can contain state too. The easiest way to do this is to create a 
closure, but if you'd rather think in objects, just override `__call__`.
"""

from canoe.filters.simple import *
from canoe.filters.utils import filter
