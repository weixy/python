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

        points = [(self.data_view.x + round(idx * unit_pixel_x),
                   self.data_view.y + self.data_view.height - round(p * unit_pixel_y)) for idx, p in enumerate(data)]

        # grp_data.add(dwg.polyline(points, fill='none', stroke=color,
        #                           style='stroke-width:2; stroke-linecap:round; linejoin:round;'))
        # path_d = 'M' + str(points[0][0]) + ',' + str(points[0][1]) + ' ' + \
        #          'L'.join(map(lambda x: str(x[0]) + ',' + str(x[1]) + ' ', points[1:len(points)]))
        path_d = 'M'
        for i in range(len(points)):
            if i % 3 == 1:
                path_d += 'C' + str(points[i][0]) + ',' + str(points[i][1]) + ' '
            else:
                path_d += str(points[i][0]) + ',' + str(points[i][1]) + ' '
        line_g = dwg.linearGradient(id=series.title, x1='0%', y1='0%', x2='0%', y2='100%')
        line_g.add_stop_color(offset='0%', color=color, opacity='0.4')
        line_g.add_stop_color(offset='100%', color='#F2F2F2', opacity='0.15')
        dwg.defs.add(line_g)

        grp_data.add(dwg.path(d=path_d, stroke=color, fill='none', style='stroke-width:1'))
        grp_data.add(dwg.path(d=path_d + 'Z', fill='url(#'+series.title+')'))
        dwg.add(grp_data)
        pass