#!/usr/bin/env python
__author__ = 'j1mw3i'
import chart


class LineChart(chart.SVGChart):

    def add_data(self, series, color, axle_x, axle_y):
        dwg = self.dwg
        grp_data = dwg.g(class_='series')
        grp_data.set_desc(desc=series.title)

        data = series.data
        unit_pixel_x = float(self.data_view.width) / axle_x
        unit_pixel_y = float(self.data_view.height) / axle_y

        points = [(self.data_view.x + round(p[0] * unit_pixel_x),
                   self.data_view.y + self.data_view.height - round(p[1] * unit_pixel_y)) for p in data]

        grp_data.add(dwg.polyline(points, fill='none', stroke=color,
                                  style='stroke-width:2; stroke-linecap:round; linejoin:round;'))

        dwg.add(grp_data)
        pass