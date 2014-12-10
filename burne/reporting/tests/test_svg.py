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
        line_chart = LineChart('reporting/_target/test_line_chart_axle.svg', (800, 400), (30, 30, 50, 50))
        line_chart.draw_background('rgb(242, 242, 242)')
        axle_style = chart.AxleStyle(
            'darkgray',
            chart.DOWN_,
            'stroke-dasharray: 1 2; stroke-width: 1;',
            'font-size: 11px; text-anchor: middle;',
        )
        line_chart.draw_axle('Time (sec)', 100, 10, axle_style)
        line_chart.save()

if __name__ == '__main__':
    unittest.main(warnings='ignore')