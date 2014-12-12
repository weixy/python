"""
Example:
index = ['id', 'Average Response Time (sec)', ...]
data = [(0, 10, ...), ...]
"""
# !/usr/bin/env python
__author__ = 'j1mw3i'


class SeriesData():
    def __init__(self, title, data):
        self.title = title
        self.data = data


class ChartData():
    def __init__(self, index, raw_data):
        self.index_list = index
        self.raw_data = raw_data

    def is_index_data_matched(self):
        return len(self.index_list) == len(self.raw_data[0])

    def get_plots(self):
        plots = []
        data = self.raw_data[0]
        id_list = [d[0] for d in self.raw_data]
        for i in range(1, len(data)):
            value_list = [d[i] for d in self.raw_data]
            plots.append(SeriesData(self.index_list[i], value_list))
        return plots