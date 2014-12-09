#!/usr/bin/env python
__author__ = 'j1mw3i'

import unittest
from xml.dom import minidom
from ..utils.svg.linechart import LineChart


class LineChartTest(unittest.TestCase):

    def test_line_chart_background(self):
        line_chart = LineChart('reporting/_target/test_line_chart.svg', 'full', (1000, 400))
        line_chart.draw_background('rgb(242, 242, 242)')
        line_chart.save()
        dom = minidom.parse(line_chart.filename)
        root = dom.documentElement
        self.assertTrue(root.nodeName == 'svg')
        grps = root.getElementsByTagName('g')
        self.assertTrue(grps[0].getAttribute('class') == 'background')
        dom.unlink()

    def test_line_chart_axle(self):
        pass

if __name__ == '__main__':
    unittest.main(warnings='ignore')