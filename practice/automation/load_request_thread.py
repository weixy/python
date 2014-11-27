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
THREAD_NUM = 4
WORKER_CYCLE = 3
LOOP_SLEEP = 0

# Statistics
ERROR_NUM = 0
LOAD_RESULTS = {
    1: {'info': ('/login/?next=/', 'GET'), 'total_num': 0, 'error_num': 0, 'durations': [], 'ave_resp': 0},
    2: {'info': ('/login/login?next=%2F', 'POST'), 'total_num': 0, 'error_num': 0, 'durations': [], 'ave_resp': 0},
    3: {'info': ('/', 'GET'), 'total_num': 0, 'error_num': 0, 'durations': [], 'ave_resp': 0},
    4: {'info': ('/business/6401/', 'GET'), 'total_num': 0, 'error_num': 0, 'durations': [], 'ave_resp': 0},
    5: {'info': ('/logout/', 'GET'), 'total_num': 0, 'error_num': 0, 'durations': [], 'ave_resp': 0},
}

millis_now = lambda: int(round(time.time() * 1000))


def update_results(results):
    global LOAD_RESULTS
    lock = threading.RLock()
    for i in range(0, len(results)):
        result_dict = LOAD_RESULTS[i+1]
        result_dict['durations'].append(results[i])
        dur_list = result_dict['durations']
        result_dict['ave_resp'] = sum(dur_list)/float(len(dur_list))
        lock.acquire()
        LOAD_RESULTS[i+1]['durations'] = dur_list
        lock.release()


def do_work(index, url):
    t = threading.currentThread()
    lock = threading.RLock()
    # print '[' + t.name + ' ' + str(index) + '] ' + url
    results = []

    try:
        client = requests.session()
        refer_url = '%s%s' % (url, '/login/?next=/')
        start = millis_now()
        response = client.get(refer_url)
        diff = millis_now() - start
        results.append(diff)
        print '[' + t.name + '.' + str(index) + \
              '.1] Extract token ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)
        csrftoken = client.cookies['csrftoken']

        login_data = dict(username='test_auto_user0' + str(index-1) + '@yellow.co.nz', password='test123', csrfmiddlewaretoken=csrftoken)
        login_url = '%s%s' % (url, '/login/login?next=%2F')
        start = millis_now()
        response = client.post(login_url, data=login_data, headers=dict(Referer=refer_url), allow_redirects=False)
        diff = millis_now() - start
        results.append(diff)
        print '[' + t.name + '.' + str(index) + \
              '.2] Login ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)
        redirect_url = response.headers['Location']

        start = millis_now()
        response = client.get(redirect_url, allow_redirects=False)
        diff = millis_now() - start
        results.append(diff)
        print '[' + t.name + '.' + str(index) + \
              '.3] Load page after login ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)

        busi_url = '%s%s' % (url, '/business/6401/')
        start = millis_now()
        response = client.get(busi_url, allow_redirects=False)
        diff = millis_now() - start
        results.append(diff)
        if response.status_code == 302 and 'Location' in response.headers:
            relocation = response.headers['Location']
            print relocation
        print '[' + t.name + '.' + str(index) + \
              '.4] Open a business ... ' + '%s (ms) ... ... %s' % (diff, response.status_code)

        logout_url = '%s%s' % (url, '/logout/')
        start = millis_now()
        response = client.get(logout_url, allow_redirects=False)
        diff = millis_now() - start
        results.append(diff)
        print '[' + t.name + '.' + str(index) + \
              '.5] Logout ... ' + '%s ... ... %s' % (diff, response.status_code)

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
    #print 'Average Time per Request (ms): ', (t2 - t1) / (WORKER_CYCLE)
    print 'Requests per Second: %.1f' % (1.0 / ((t2 - t1) / (THREAD_NUM * WORKER_CYCLE) * 1000))
    #print 'Error Number: ', ERROR_NUM
    print '------------------------------------------------------------'
    print 'REQUEST\t\t\tACT_TYPE\tREQ_NUM\t\tAVG_RESP\tMAX_RESP\tMIN_RESP'
    print '%-23s %s\t\t%i\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_RESULTS[1]['info'][0], LOAD_RESULTS[1]['info'][1], LOAD_RESULTS[1]['total_num'], LOAD_RESULTS[1]['ave_resp'], max(LOAD_RESULTS[1]['durations']), min(LOAD_RESULTS[1]['durations']))
    print '%-23s %s\t\t%i\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_RESULTS[2]['info'][0], LOAD_RESULTS[2]['info'][1], LOAD_RESULTS[2]['total_num'], LOAD_RESULTS[2]['ave_resp'], max(LOAD_RESULTS[2]['durations']), min(LOAD_RESULTS[2]['durations']))
    print '%-23s %s\t\t%i\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_RESULTS[3]['info'][0], LOAD_RESULTS[3]['info'][1], LOAD_RESULTS[3]['total_num'], LOAD_RESULTS[3]['ave_resp'], max(LOAD_RESULTS[3]['durations']), min(LOAD_RESULTS[3]['durations']))
    print '%-23s %s\t\t%i\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_RESULTS[4]['info'][0], LOAD_RESULTS[4]['info'][1], LOAD_RESULTS[4]['total_num'], LOAD_RESULTS[4]['ave_resp'], max(LOAD_RESULTS[4]['durations']), min(LOAD_RESULTS[4]['durations']))
    print '%-23s %s\t\t%i\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_RESULTS[5]['info'][0], LOAD_RESULTS[5]['info'][1], LOAD_RESULTS[5]['total_num'], LOAD_RESULTS[5]['ave_resp'], max(LOAD_RESULTS[5]['durations']), min(LOAD_RESULTS[5]['durations']))

if __name__ == '__main__':
    main()