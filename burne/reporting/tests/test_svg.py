#!/usr/bin/env python
__author__ = 'j1mw3i'

import unittest
from xml.dom import minidom
from ..utils.svg.linechart import LineChart
from ..utils.svg import chart


class LineChartTest(unittest.TestCase):

    def test_line_chart_background(self):
        line_chart = LineChart('reporting/_target/test_line_chart.svg', (1000, 400))
        line_chart.draw_background('rgb(242, 242, 242)')
        line_chart.save()
        dom = minidom.parse(line_chart.filename)
        root = dom.documentElement
        self.assertTrue(root.nodeName == 'svg')
        grps = root.getElementsByTagName('g')
        self.assertTrue(grps[0].getAttribute('class') == 'background')
        dom.unlink()

    def test_line_chart_axle(self):
        line_chart = LineChart('reporting/_target/test_line_chart_axle.svg', (800, 400), (30, 40, 50, 50))
        line_chart.draw_background('rgb(242, 242, 242)')
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.DOWN_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
        )
        line_chart.draw_axle('Time (sec)', 100, 10, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.LEFT_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
        )
        line_chart.draw_axle('Current Threads', 50, 5, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.UP_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
        )
        line_chart.draw_axle('Current Users', 20, 5, axle_style)
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.RIGHT_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-family: Arial; kerning: 1; font-size: 11px; fill: darkgray; text-anchor: middle;',
        )
        line_chart.draw_axle('Current Threads', 70, 10, axle_style)
        line_chart.save()

if __name__ == '__main__':
    unittest.main(warnings='ignore')