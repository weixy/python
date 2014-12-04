__author__ = 'y981821'

import argparse
import csv
import math
import requests
import threading
import time

# Targets
ENV = 'staging'
TARGET_URL = {
    'uat': 'http://sem.uat.ytech.co.nz',
    'staging': 'https://staging.sem.yellow.co.nz',
    'production': 'https://sem.yellow.co.nz'
}

# Configuration
THREAD_NUM = 2
THREAD_BATCH = 1
THREAD_REPEAT = 1
LOOP_SLEEP = 10

# Steps
TEST_STEPS = [
    {'req_txt': 'TOTAL', 'req_type': 'ALL'},
    {'req_txt': '/login/?next=/', 'req_type': 'GET'},
    {'req_txt': '/login/login?next=%2F', 'req_type': 'POST'},
    {'req_txt': '/', 'req_type': 'GET'},
    {'req_txt': '/business/6401/', 'req_type': 'GET'},
    {'req_txt': '/logout', 'req_type': 'GET'},
]


# Statistics
class RequestStatistics():
    def __init__(self, req_text, req_type):
        self.req_text = req_text
        self.req_type = req_type
        self.error_num = 0
        self.ave_resp = 0.0
        self.min_resp = 0.0
        self.max_resp = 0.0
ERROR_NUM = 0
LOAD_STATISTICS = [RequestStatistics(step['req_txt'], step['req_type']) for step in TEST_STEPS]
# LOAD_STATISTICS = {
#     1: {'info': ('/login/?next=/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
#     2: {'info': ('/login/login?next=%2F', 'POST'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
#     3: {'info': ('/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
#     4: {'info': ('/business/6401/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
#     5: {'info': ('/logout/', 'GET'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
#     6: {'info': ('TOTAL', 'ALL'), 'error_num': 0, 'ave_resp': 0, 'min_resp': 0, 'max_resp': 0},
# }

LOAD_RECORDS = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
}

millis_now = lambda: int(round(time.time() * 1000))


def calculate_result(results):
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


class LoadRequest():
    def __init__(self, url, act_type, data=None, headers=None, allow_redirects=False):
        self.url = url
        self.action_type = act_type
        self.data = data
        self.headers = headers
        self.redirects = allow_redirects

    def request(self):
        client = requests.session()
        start = millis_now()
        response = client.get(self.url)
        end = millis_now()
        return client, response, start, end


class LoadThread(threading.Thread):
    def __init__(self, repeat):
        threading.Thread.__init__(self)
        self.results = []
        self.update = calculate_result
        self.repeat_times = repeat

    def do_work(self):
        domain = TARGET_URL[ENV]
        total_start = millis_now()

        # Step 1
        s = TEST_STEPS[1]
        start_url = domain + s['req_txt']
        step_req = LoadRequest(start_url, s['req_type'])
        client, response, start, end = step_req.request()
        self.results.append((start, end))
        print '>>> [%s] Step 1: Extract token, spent %s (ms) with code %s' % (
            self.name, end-start, response.status_code)

        token = client.cookies['csrftoken']

        # Step 2
        login_data = dict(
            username='developers@finda.co.nz',
            password='QAWSEDRFTG', csrfmiddlewaretoken=token
        )
        s = TEST_STEPS[2]
        step_req = LoadRequest(domain + s['req_txt'], s['req_type'], login_data, dict(Referer=start_url))
        client, response, start, end = step_req.request()
        self.results.append((start, end))
        print '>>> [%s] Step 2: Login Murray, spent %s (ms) with code %s' % (
            self.name, end-start, response.status_code)

        redirect_url = response.headers['Location']

        # Step 3
        s = TEST_STEPS[3]
        step_req = LoadRequest(redirect_url, s['req_type'])
        client, response, start, end = step_req.request()
        self.results.append((start, end))
        print '>>> [%s] Step 3: Load start page with SEM Dashboard, spent %s (ms) with code %s' % (
            self.name, end-start, response.status_code)

        total_end = millis_now()
        self.results.append((total_start, total_end))
        self.update(self.results)


def do_work(index, url):
    t = threading.currentThread()
    results = []

    try:
        client = requests.session()
        refer_url = '%s%s' % (url, '/login/?next=/')
        total_start = millis_now()
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
        total_end = millis_now()
        results.append((start, end))
        print '[' + t.name + '.' + str(index) + \
              '.5] Logout ... ' + '%s ... ... %s' % (end-start, response.status_code)

        results.append((total_start, total_end))
        calculate_result(results)

    except Exception as e:
        print 'Failed with exception \'%s\': \n%s' % (e.__class__, e.message)
        global ERROR_NUM
        ERROR_NUM += 1


def working():
    t = threading.currentThread()
    print '[' + t.name + '] Sub Thread Begin'

    i = 0
    while i < THREAD_REPEAT:
        i += 1
        # do_work(i, TARGET_URL['uat'])
        do_work(i, TARGET_URL['staging'])
        # do_work(i, TARGET_URL['production'])
        # sleep(LOOP_SLEEP)

    print '[' + t.name + '] Sub Thread End'


def main():
    t1 = millis_now()

    threads = []

    for j in range(THREAD_BATCH):
        for i in range(THREAD_NUM):
            t = threading.Thread(target=working, name='T' + str(j) + '-' + str(i))
            # t.daemon = True
            threads.append(t)
            t.start()
        time.sleep(LOOP_SLEEP)
    for t in threads:
        if t.isAlive():
            t.join()
    print 'main thread end'

    t2 = millis_now()
    print '============================================================='
    print 'Execution Number: ', THREAD_NUM, '*', THREAD_REPEAT, '*', THREAD_BATCH, \
        '=', THREAD_NUM * THREAD_REPEAT * THREAD_BATCH
    print 'Total Time (ms): ', t2 - t1
    # print 'Requests per micro-second: %.1f' % ((1.0 * THREAD_NUM * THREAD_REPEAT * THREAD_BATCH) / (t2 - t1))
    print '------------------------------------------------------------'
    print 'REQUEST\t\t\tACT_TYPE\tAVG_RESP\tMIN_RESP\tMAX_RESP'
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[1]['info'][0], LOAD_STATISTICS[1]['info'][1], LOAD_STATISTICS[1]['ave_resp'], LOAD_STATISTICS[1]['min_resp'], LOAD_STATISTICS[1]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[2]['info'][0], LOAD_STATISTICS[2]['info'][1], LOAD_STATISTICS[2]['ave_resp'], LOAD_STATISTICS[2]['min_resp'], LOAD_STATISTICS[2]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[3]['info'][0], LOAD_STATISTICS[3]['info'][1], LOAD_STATISTICS[3]['ave_resp'], LOAD_STATISTICS[3]['min_resp'], LOAD_STATISTICS[3]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[4]['info'][0], LOAD_STATISTICS[4]['info'][1], LOAD_STATISTICS[4]['ave_resp'], LOAD_STATISTICS[4]['min_resp'], LOAD_STATISTICS[4]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[5]['info'][0], LOAD_STATISTICS[5]['info'][1], LOAD_STATISTICS[5]['ave_resp'], LOAD_STATISTICS[5]['min_resp'], LOAD_STATISTICS[5]['max_resp'])
    print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (LOAD_STATISTICS[6]['info'][0], LOAD_STATISTICS[6]['info'][1], LOAD_STATISTICS[6]['ave_resp'], LOAD_STATISTICS[6]['min_resp'], LOAD_STATISTICS[6]['max_resp'])
    print '------------------------------------------------------------'
    # print LOAD_RECORDS
    ave_resp_ps = [(0, 0.000, 0.000, 0.000, 0)]
    td = int(math.ceil((t2 - t1) / 1000.0))
    for t in range(1, td + 1):
        t_sum = []
        finished_num = 0
        working_num = 0
        record_list = LOAD_RECORDS[6]
        ts = t1 + t * 1000
        for v in record_list:
            if v[1] <= ts:
                finished_num += 1
                t_sum.append(v[1] - v[0])
            if v[0] <= ts <= v[1]:
                working_num += 1
        if finished_num == THREAD_NUM * THREAD_REPEAT * THREAD_BATCH:
            ave_resp_ps.append((t, 0.000, 0.000, 0.000, 0))
        elif finished_num > 0:
            ave_resp_ps.append((
                t,
                float('%.3f' % (float(sum(t_sum))/(finished_num*1000))),
                float('%.3f' % (min(t_sum)/1000.0)),
                float('%.3f' % (max(t_sum)/1000.0)),
                working_num))
        else:
            pre_ave_resp = ave_resp_ps[-1][1]
            ave_resp_ps.append((t, pre_ave_resp, 0, 0, working_num))
    # print ave_resp_ps
    with open('ave_resp_persec.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(ave_resp_ps)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a load test on Hydrogen API')
    parser.add_argument('--env', dest='env', default='staging',
                        help='Set the environment to run on. (uat/staging/production).')
    args = parser.parse_args()
    ENV = args.env
    # main()
    # for i in LOAD_STATISTICS:
    #     print i.req_text + ', ' + i.req_type + ', ' + str(i.ave_resp)