__author__ = 'y981821'

import time
import requests

URL = 'https://staging.sem.yellow.co.nz'
client = requests.session()
millis_now = lambda: int(round(time.time() * 1000))

refer_url = '%s%s' % (URL, '/login/?next=/')
start = millis_now()
client.get(refer_url)
diff = millis_now() - start
print diff
csrftoken = client.cookies['csrftoken']

login_data = dict(username='developers@finda.co.nz', password='QAWSEDRFTG', csrfmiddlewaretoken=csrftoken)
login_url = '%s%s' % (URL, '/login/login?next=%2F')
start = millis_now()
response = client.post(login_url, data=login_data, headers=dict(Referer=refer_url))
diff = millis_now() - start
print diff

alerts_url = '%s%s' % (URL, '/alerts/')
start = millis_now()
response = client.get(alerts_url)
diff = millis_now() - start
print diff
print response.status_code
