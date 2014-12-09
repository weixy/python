"""
Example:
index = ['id', 'Average Response Time (sec)', ...]
data = [(0, 10, ...), ...]
"""
# !/usr/bin/env python
__author__ = 'j1mw3i'


class ReportData():
    def __init__(self, index, raw_data):
        self.index_list = index
        self.data_table = raw_data

    def is_index_data_matched(self):
        return len(self.index_list) == len(self.data_table[0])

    def separated_tables(self):
        sep_tables = []
        data = self.data_table[0]
        id_list = [d[0] for d in self.data_table]
        for i in range(1, len(data)):
            value_list = [d[i] for d in self.data_table]
            sep_tables.append({'title': self.index_list[i], 'data': (zip(id_list, value_list))})
        return sep_tables