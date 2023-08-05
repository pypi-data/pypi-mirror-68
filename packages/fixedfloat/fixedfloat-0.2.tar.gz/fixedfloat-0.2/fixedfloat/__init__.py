# -*- coding: utf-8 -*-

import sys
from .api import FixedFloatAPI

if not sys.version_info < (3, 6):
    from .apiasync import FixedFloatAPIAsync
