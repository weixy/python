__author__ = 'y981821'

import time
import requests

URL = 'https://sem.yellow.co.nz'
client = requests.session()
millis_now = lambda: int(round(time.time() * 1000))

refer_url = '%s%s' % (URL, '/login/?next=/')
start = millis_now()
response = client.get(refer_url)
diff = millis_now() - start
print '%s ... ... %s' % (diff, response.status_code)
csrftoken = client.cookies['csrftoken']

login_data = dict(username='developers@finda.co.nz', password='QAWSEDRFTG', csrfmiddlewaretoken=csrftoken)
login_url = '%s%s' % (URL, '/login/login?next=%2F')
start = millis_now()
response = client.post(login_url, data=login_data, headers=dict(Referer=refer_url), allow_redirects=False)
diff = millis_now() - start
print '%s ... ... %s' % (response.elapsed.total_seconds() * 1000, response.status_code)
redirect_url = response.headers['Location']

start = millis_now()
response = client.get(redirect_url, allow_redirects=False)
diff = millis_now() -start
print '%s ... ... %s' % (response.elapsed.total_seconds() * 1000, response.status_code)

busi_url = '%s%s' % (URL, '/business/6401/')
start = millis_now()
response = client.get(busi_url, allow_redirects=False)
diff = millis_now() - start
if response.status_code == 302 and 'Location' in response.headers:
    relocation = response.headers['Location']
    print relocation

print '%s ... ... %s' % (diff, response.status_code)

alerts_url = '%s%s' % (URL, '/alerts/')
start = millis_now()
response = client.get(alerts_url, allow_redirects=False)
diff = millis_now() - start
print '%s ... ... %s' % (diff, response.status_code)

# logout_url = '%s%s' % (URL, '/logout/')
# start = millis_now()
# response = client.get(logout_url, allow_redirects=False)
# diff = millis_now() - start
# print '%s ... ... %s' % (diff, response.status_code)
