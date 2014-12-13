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
        path_d = 'M' + str(points[0][0]) + ',' + str(points[0][1]) + ' ' + \
                 'L'.join(map(lambda x: str(x[0]) + ',' + str(x[1]) + ' ', points[1:len(points)]))
        # path_d = 'M'
        # for i in range(len(points)):
        #     if i % 3 == 1:
        #         path_d += 'C' + str(points[i][0]) + ',' + str(points[i][1]) + ' '
        #     else:
        #         path_d += str(points[i][0]) + ',' + str(points[i][1]) + ' '
        line_g = dwg.linearGradient(id=series.title.replace(' ', ''), x1='0%', y1='0%', x2='0%', y2='100%')
        line_g.add_stop_color(offset='0%', color=color, opacity='0.4')
        line_g.add_stop_color(offset='100%', color='#F9FBFB', opacity='0.15')
        dwg.defs.add(line_g)

        grp_data.add(dwg.path(d=path_d, stroke=color, fill='none', style='stroke-width:1.1'))
        grp_data.add(dwg.path(d=path_d + 'Z', fill='url(#'+series.title.replace(' ', '')+')'))

        for i in range(len(points)):
            circle = dwg.circle(class_='data_cycle', center=points[i], r=3, id=i,
                                fill='white', stroke='#ff6600',
                                style='display: none; stroke-width: 2;')
            circle.set_desc(title=series.title, desc=data[i])
            grp_data.add(circle)
        dwg.add(grp_data)

    def add_data_trigger(self, axle):
        dwg = self.dwg
        grp_trigger = dwg.g(class_='trigger_grp')
        if axle.style.position == chart.TOP_ or axle.style.position == chart.BOTTOM_:
            rect_width = float(self.data_view.width) / axle.gradation_max
            rect_height = self.data_view.height
            offset = (1, 0)
        else:
            rect_width = self.data_view.width
            rect_height = float(self.data_view.height) / axle.gradation_max
            offset = (0, 1)
        x = self.data_view.x - offset[0] * rect_width * 0.5
        y = self.data_view.y - offset[1] * rect_height * 0.5
        for i in range(axle.gradation_max + 1):
            rect = dwg.rect(class_='data_trigger', insert=(x, y), size=(rect_width, rect_height),
                            style='stroke: none; fill: transparent;')
            rect.set_desc(desc=i)
            grp_trigger.add(rect)
            x += offset[0] * rect_width
            y += offset[1] * rect_height
        dwg.add(grp_trigger)