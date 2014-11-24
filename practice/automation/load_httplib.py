__author__ = 'y981821'

import httplib
import urllib
import time

URL = 'staging.sem.yellow.co.nz'
millis_now = lambda: int(round(time.time() * 1000))

refer_url = '%s%s' % (URL, '/login/?next=/')
print refer_url
conn = httplib.HTTPSConnection(URL)
start_time = millis_now()
conn.request('GET', '/login/?next=/')
request_time = millis_now()
resp = conn.getresponse()
response_time = millis_now()
conn.close()
transfer_time = millis_now()
print '%f ms' % (request_time - start_time)
print '%f ms' % (transfer_time - request_time)
print '%f ms' % (transfer_time - start_time)
print resp.status
print resp.msg
print resp.getheader('location')