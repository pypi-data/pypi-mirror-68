# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] < 3:
    raise ImportError('Python < 3.0 is unsupported.')

from .binding import Binder
from .step import Step

__title__ = 'monapy'
__description__ = 'Declarative programming tools'
__version__ = '0.3.4'
__author__ = 'Andriy Stremeluk'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020 Andriy Stremeluk'

__all__ = ['Step', 'Binder']
