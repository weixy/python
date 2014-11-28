__author__ = 'y981821'

import time
import requests
import threading
from time import sleep

# Targets
TARGET_URL = {
    'staging': 'https://staging.sem.yellow.co.nz',
    'production': 'https://sem.yellow.co.nz'
}

# Configuration
THREAD_NUM = 4
WORKER_CYCLE = 3
LOOP_SLEEP = 0

# Statistics
ERROR_NUM = 0
LOAD_STATISTICS = {
    1: {'info': ('/login/?next=/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
    2: {'info': ('/login/login?next=%2F', 'POST'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
    3: {'info': ('/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
    4: {'info': ('/business/6401/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
    5: {'info': ('/logout/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
}

LOAD_RECORDS = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
}

millis_now = lambda: int(round(time.time() * 1000))


def update_results(results):
    global LOAD_STATISTICS
    lock = threading.RLock()
    for i in range(0, len(results)):
        statistics_dict = LOAD_STATISTICS[i+1]
        records_list = LOAD_RECORDS[i+1]
        records_list.append(results[i])
        dur_list = [v[1] - v[0] for v in records_list]
        statistics_dict['ave_resp'] = sum(dur_list)/float(len(dur_list))
        statistics_dict['min_resp'] = min(dur_list)
        statistics_dict['max_resp'] = max(dur_list)
        lock.acquire()
        LOAD_STATISTICS[i+1] = statistics_dict
        LOAD_RECORDS[i+1] = records_list
        lock.release()


def do_work(index, url):
    t = threading.currentThread()
    results = []

    try:
        client = requests.session()
        refer_url = '%s%s' % (url, '/login/?next=/')
        start = millis_now()
        response = client.get(refer_url)
        end = millis_now()
        results.append((start, end))
        print '[' + t.name + '.' + str(index) + \
              '.1] Extract token ... ' + '%s (ms) ... ... %s' % (end-start, response.status_code)
        csrftoken = client.cookies['csrftoken']

        login_data = dict(
            username='test_auto_user0' + str(index-1) + '@yellow.co.nz',
            password='test123', csrfmiddlewaretoken=csrftoken
        )
        login_url = '%s%s' % (url, '/login/login?next=%2F')
        start = millis_now()
        response = client.post(login_url, data=login_data, headers=dict(Referer=refer_url), allow_redirects=False)
        end = millis_now()
        results.append((start, end))
        print '[' + t.name + '.' + str(index) + \
              '.2] Login ... ' + '%s (ms) ... ... %s' % (end-start, response.status_code)
        redirect_url = response.headers['Location']

        start = millis_now()
        response = client.get(redirect_url, allow_redirects=False)
        end = millis_now()
        results.append((start, end))
        print '[' + t.name + '.' + str(index) + \
              '.3] Load page after login ... ' + '%s (ms) ... ... %s' % (end-start, response.status_code)

        busi_url = '%s%s' % (url, '/business/6401/')
        start = millis_now()
        response = client.get(busi_url, allow_redirects=False)
        end = millis_now()
        results.append((start, end))
        if response.status_code == 302 and 'Location' in response.headers:
            relocation = response.headers['Location']
            print relocation
        print '[' + t.name + '.' + str(index) + \
              '.4] Open a business ... ' + '%s (ms) ... ... %s' % (end-start, response.status_code)

        logout_url = '%s%s' % (url, '/logout/')
        start = millis_now()
        response = client.get(logout_url, allow_redirects=False)
        end = millis_now()
        results.append((start, end))
        print '[' + t.name + '.' + str(index) + \
              '.5] Logout ... ' + '%s ... ... %s' % (end-start, response.status_code)

        update_results(results)

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
    print '============================================================='
    print 'Execution Number: ', THREAD_NUM, '*', WORKER_CYCLE, '=', THREAD_NUM * WORKER_CYCLE
    print 'Total Time (ms): ', t2 - t1
    print 'Requests per Second: %.1f' % (1.0 / ((t2 - t1) / (THREAD_NUM * WORKER_CYCLE) * 1000))
    print '------------------------------------------------------------'
    print 'REQUEST\t\t\tACT_TYPE\tAVG_RESP\tMIN_RESP\tMAX_RESP'
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[1]['info'][0], LOAD_STATISTICS[1]['info'][1], LOAD_STATISTICS[1]['ave_resp'], LOAD_STATISTICS[1]['min_resp'], LOAD_STATISTICS[1]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[2]['info'][0], LOAD_STATISTICS[2]['info'][1], LOAD_STATISTICS[2]['ave_resp'], LOAD_STATISTICS[2]['min_resp'], LOAD_STATISTICS[2]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[3]['info'][0], LOAD_STATISTICS[3]['info'][1], LOAD_STATISTICS[3]['ave_resp'], LOAD_STATISTICS[3]['min_resp'], LOAD_STATISTICS[3]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[4]['info'][0], LOAD_STATISTICS[4]['info'][1], LOAD_STATISTICS[4]['ave_resp'], LOAD_STATISTICS[4]['min_resp'], LOAD_STATISTICS[4]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[5]['info'][0], LOAD_STATISTICS[5]['info'][1], LOAD_STATISTICS[5]['ave_resp'], LOAD_STATISTICS[5]['min_resp'], LOAD_STATISTICS[5]['max_resp'])
    print '------------------------------------------------------------'
    print LOAD_RECORDS

if __name__ == '__main__':
    main()