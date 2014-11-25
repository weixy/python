__author__ = 'y981821'

import time
import requests
import threading
from Queue import Queue
from time import sleep

# Targets
TARGET_URL = {
    'staging': 'https://staging.sem.yellow.co.nz',
    'production': 'https://sem.yellow.co.nz'
}

# Configuration
THREAD_NUM = 5
WORKER_CYCLE = 2
LOOP_SLEEP = 0

# Statistics
ERROR_NUM = 0

millis_now = lambda: int(round(time.time() * 1000))


def do_work(index, url):
    t = threading.currentThread()
    print '[' + t.name + ' ' + str(index) + '] ' + url

    try:
        client = requests.session()
        refer_url = '%s%s' % (url, '/login/?next=/')
        start = millis_now()
        response = client.get(refer_url)
        diff = millis_now() - start
        print '[' + t.name + '.' + str(index) + \
              '.1] Extract token ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)
        csrftoken = client.cookies['csrftoken']

        login_data = dict(username='developers@finda.co.nz', password='QAWSEDRFTG', csrfmiddlewaretoken=csrftoken)
        login_url = '%s%s' % (url, '/login/login?next=%2F')
        start = millis_now()
        response = client.post(login_url, data=login_data, headers=dict(Referer=refer_url), allow_redirects=False)
        diff = millis_now() - start
        print '[' + t.name + '.' + str(index) + '.2] Login ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)
        redirect_url = response.headers['Location']

        start = millis_now()
        response = client.get(redirect_url, allow_redirects=False)
        diff = millis_now() - start
        print '[' + t.name + '.' + str(index) + \
              '.3] Load page after login ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)

        busi_url = '%s%s' % (url, '/business/6401/')
        start = millis_now()
        response = client.get(busi_url, allow_redirects=False)
        diff = millis_now() - start
        if response.status_code == 302 and 'Location' in response.headers:
            relocation = response.headers['Location']
            print relocation
        print '[' + t.name + '.' + str(index) + \
              '.4] Open a business ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)

    except Exception as e:
        print 'Failed with exception \'%s\': \n%s' % (e.__class__, e.message)
        global ERROR_NUM
        ERROR_NUM += 1


def working():
    t = threading.currentThread()
    print '[' + t.name + '] Sub Thread Begin'

    i = 0
    while i < WORKER_CYCLE:
        i += 1
        do_work(i, TARGET_URL['staging'])
        sleep(LOOP_SLEEP)

    print '[' + t.name + '] Sub Thread End'


def main():
    t1 = millis_now()

    threads = []

    for i in range(THREAD_NUM):
        t = threading.Thread(target=working, name='T' + str(i))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print 'main thread end'

    t2 = millis_now()
    print '=========================================='
    print 'Task Number: ', THREAD_NUM, '*', WORKER_CYCLE, '=', THREAD_NUM * WORKER_CYCLE
    print 'Total Time (ms): ', t2 - t1
    print 'Average Time per Request (ms): ', (t2 - t1) / (THREAD_NUM * WORKER_CYCLE)
    print 'Requests per Second: ', 1.0 / ((t2 - t1) / THREAD_NUM * WORKER_CYCLE) * 1000
    print 'Error Number: ', ERROR_NUM

if __name__ == '__main__':
    main()