#!/usr/bin/env python
import os

CONSTELLATION = os.environ.get('CONSTELLATION', 'staging')
WEB_DRIVER = os.environ.get('WEB_DRIVER', 'firefox')
HTTP_SECURE = os.environ.get('HTTP_SECURE', False)
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
