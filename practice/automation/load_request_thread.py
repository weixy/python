__author__ = 'y981821'

import argparse
import csv
import math
import requests
import threading
import time

# Targets
ENV = 'staging'
REPORT = 'csv'
TARGET_URL = {
    'uat': 'http://sem.uat.ytech.co.nz',
    'staging': 'https://staging.sem.yellow.co.nz',
    'production': 'https://sem.yellow.co.nz'
}

# Configuration
THREAD_NUM = 10
THREAD_BATCH = 3
THREAD_REPEAT = 2
LOOP_SLEEP = 15

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
LOAD_RECORDS = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
}

millis_now = lambda: int(round(time.time() * 1000))


def calculate_result(results):
    global LOAD_STATISTICS
    lock = threading.RLock()
    for i in range(0, len(results)):
        statistics = LOAD_STATISTICS[i]
        records_list = LOAD_RECORDS[i]
        records_list.append(results[i])
        dur_list = [v[1] - v[0] for v in records_list]
        statistics.ave_resp = sum(dur_list)/float(len(dur_list))
        statistics.min_resp = min(dur_list)
        statistics.max_resp = max(dur_list)
        lock.acquire()
        LOAD_STATISTICS[i] = statistics
        LOAD_RECORDS[i] = records_list
        lock.release()


class LoadRequest():
    def __init__(self, url, act_type, data=None, headers=None, allow_redirects=False):
        self.url = url
        self.action_type = act_type
        self.data = data
        self.headers = headers
        self.redirects = allow_redirects

    def request(self, client):
        if client is None:
            client = requests.session()
        start = millis_now()
        if self.action_type.lower() == 'GET'.lower():
            response = client.get(self.url, allow_redirects=self.redirects)
        elif self.action_type.lower() == 'POST'.lower():
            response = client.post(self.url, data=self.data, headers=self.headers, allow_redirects=self.redirects)
        else:
            response = None
        end = millis_now()
        return client, response, start, end


class LoadThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        # self.results = []
        self.update = calculate_result
        self.name = name

    def do_work(self):
        domain = TARGET_URL[ENV]
        total_start = millis_now()
        client = None
        try:
            # Step 1
            s = TEST_STEPS[1]
            start_url = domain + s['req_txt']
            step_req = LoadRequest(start_url, s['req_type'])
            client, response, start, end = step_req.request(client)
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
            step_req = LoadRequest(
                domain + s['req_txt'],
                s['req_type'],
                data=login_data,
                headers=dict(Referer=start_url),
            )
            client, response, start, end = step_req.request(client)
            self.results.append((start, end))
            print '>>> [%s] Step 2: Login Murray, spent %s (ms) with code %s' % (
                self.name, end-start, response.status_code)

            redirect_url = response.headers['Location']

            # Step 3
            s = TEST_STEPS[3]
            step_req = LoadRequest(redirect_url, s['req_type'])
            client, response, start, end = step_req.request(client)
            self.results.append((start, end))
            print '>>> [%s] Step 3: Load start page with SEM Dashboard, spent %s (ms) with code %s' % (
                self.name, end-start, response.status_code)

            # Step 4
            s = TEST_STEPS[4]
            step_req = LoadRequest(domain + s['req_txt'], s['req_type'])
            client, response, start, end = step_req.request(client)
            self.results.append((start, end))
            print '>>> [%s] Step 4: Open a business, spent %s (ms) with code %s' % (
                self.name, end-start, response.status_code)

            # Step 5
            s = TEST_STEPS[5]
            step_req = LoadRequest(domain + s['req_txt'], s['req_type'])
            client, response, start, end = step_req.request(client)
            self.results.append((start, end))
            print '>>> [%s] Step 5: Logout Murray, spent %s (ms) with code %s' % (
                self.name, end-start, response.status_code)

            total_end = millis_now()
            self.results.insert(0, (total_start, total_end))
            self.update(self.results)
        except Exception as e:
            print 'Failed with exception \'%s\': \n%s' % (e.__class__, e.message)
            global ERROR_NUM
            ERROR_NUM += 1

    def run(self):
        t = threading.currentThread()
        print '>> Sub thread [%s] begin' % t.name
        i = 0
        while i < THREAD_REPEAT:
            i += 1
            self.results = []
            self.do_work()
        print '>> Sub thread [%s] end' % t.name


def main():
    t1 = millis_now()

    threads = []

    for j in range(THREAD_BATCH):
        for i in range(THREAD_NUM):
            t = LoadThread(name='T' + str(j) + '-' + str(i))
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
    for s in LOAD_STATISTICS:
        print '%-23s %s\t\t%.1f\t\t%.1f\t\t%.1f' % (s.req_text, s.req_type, s.ave_resp, s.min_resp, s.max_resp)
    print '------------------------------------------------------------'
    # print LOAD_RECORDS
    ave_resp_ps = [(0.0, 0.000, 0.000, 0.000, 0)]
    t_step = 1
    td = int(math.ceil((t2 - t1) / (t_step * 1000.0)))
    for t in range(1, td + 1):
        t_sum = []
        finished_num = 0
        working_num = 0
        record_list = LOAD_RECORDS[0]
        ts = t1 + t * t_step * 1000
        for v in record_list:
            if v[1] <= ts:
                finished_num += 1
                t_sum.append(v[1] - v[0])
            if v[0] <= ts <= v[1]:
                working_num += 1
        if finished_num == THREAD_NUM * THREAD_REPEAT * THREAD_BATCH:
            ave_resp_ps.append((t * t_step, 0.000, 0.000, 0.000, 0))
        elif finished_num > 0:
            ave_resp_ps.append((
                t * t_step,
                float('%.3f' % (float(sum(t_sum))/(finished_num*1000))),
                float('%.3f' % (min(t_sum)/1000.0)),
                float('%.3f' % (max(t_sum)/1000.0)),
                working_num))
        else:
            pre_ave_resp = ave_resp_ps[-1][1]
            ave_resp_ps.append((t * t_step, pre_ave_resp, 0, 0, working_num))
    # print ave_resp_ps
    with open('ave_resp_persec.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(ave_resp_ps)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a load test on Hydrogen API')
    parser.add_argument('-e', '--env', dest='env', default='staging',
                        help='Set the environment to run on (uat/staging/production).')
    parser.add_argument('-r', '--report', dest='report', default='csv',
                        help='Set the report format as (csv/json/html).')
    args = parser.parse_args()
    ENV = args.env
    REPORT = args.report
    main()