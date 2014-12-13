#!/usr/bin/env python
__author__ = 'j1mw3i'

import unittest

from xml.dom import minidom
from ..utils.svg.linechart import LineChart
from ..utils.svg import chart
from ..utils.data import data
from ..tests import test_data


class LineChartTest(unittest.TestCase):

    def test_line_chart_background(self):
        line_chart = LineChart('reporting/_target/test_line_chart.svg', (1000, 400))
        line_chart.add_background('rgb(242, 242, 242)')
        line_chart.save()
        dom = minidom.parse(line_chart.filename)
        root = dom.documentElement
        self.assertTrue(root.nodeName == 'svg')
        groups = root.getElementsByTagName('g')
        self.assertTrue(groups[0].getAttribute('class') == 'background')
        dom.unlink()

    def test_line_chart_axle(self):
        line_chart = LineChart('reporting/_target/test_line_chart_axle.svg', (800, 400), (40, 40, 50, 50))
        line_chart.add_background('rgb(242, 242, 242)')
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.BOTTOM_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; stroke: none; text-anchor: middle;',
            show_gradation_line=True,
        )
        line_chart.add_axle('Time (sec)', 100, 10, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.LEFT_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; stroke: none; text-anchor: middle;',
        )
        line_chart.add_axle('Current Threads', 50, 5, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.TOP_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; stroke: none; text-anchor: middle;',
        )
        line_chart.add_axle('Current Users', 20, 5, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.RIGHT_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; stroke: none; text-anchor: middle;',
        )
        line_chart.add_axle('Response Time (ms)', 70, 10, axle_style)
        line_chart.save()
        dom = minidom.parse(line_chart.filename)
        root = dom.documentElement
        self.assertTrue(root.nodeName == 'svg')
        groups = root.getElementsByTagName('g')
        for i in range(1, len(groups)):
            self.assertTrue(groups[i].getAttribute('class') == 'axle')
        descs = groups[1].getElementsByTagName('desc')
        self.assertTrue(descs[0].firstChild.nodeValue == 'Time (sec)')
        descs = groups[2].getElementsByTagName('desc')
        self.assertTrue(descs[0].firstChild.nodeValue == 'Current Threads')
        descs = groups[3].getElementsByTagName('desc')
        self.assertTrue(descs[0].firstChild.nodeValue == 'Current Users')
        descs = groups[4].getElementsByTagName('desc')
        self.assertTrue(descs[0].firstChild.nodeValue == 'Response Time (ms)')
        dom.unlink()

    def test_line_chart_data(self):
        raw_data = test_data.extract_csv('reporting/samples/sample_data.csv')
        data_dict = test_data.SAMPLE_DATA_INDEX
        chart_data = data.ChartData(data_dict, raw_data)
        plots = chart_data.get_plots()
        line_chart = LineChart('reporting/_target/test_line_chart_data.svg', (600, 200), (40, 40, 50, 50))
        line_chart.add_background('#F9FBFB')
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.BOTTOM_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; font-size: 11px; fill: darkgray; stroke: none; text-anchor: middle;',
            show_gradation_line=True,
        )
        axle1 = line_chart.add_axle('Time (sec)', 110, 10, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.LEFT_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; font-size: 11px; fill: #5dc4cd; stroke: none; text-anchor: middle;',
            show_line=False,
        )
        line_chart.add_axle('Current Threads', 35, 5, axle_style)

        axle_style = chart.AxleStyle(
            'darkgray',
            chart.RIGHT_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; font-size: 11px; fill: darkgray; text-anchor: middle;',
            'font-family: Arial; font-size: 11px; fill: #669900; stroke: none; text-anchor: middle;',
            show_line=False,
        )
        line_chart.add_axle('Average Response Time (ms)', 40, 5, axle_style)

        line_chart.add_data(plots[3], '#5dc4cd', 110, 35)
        line_chart.add_data(plots[0], '#669900', 110, 40)
        line_chart.add_data_trigger(axle1)
        line_chart.save()


if __name__ == '__main__':
    unittest.main()