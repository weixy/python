#!/usr/bin/env python
__author__ = 'j1mw3i'
import svgwrite


class AxleStyle():

    _UP_ = 'up'
    _DOWN_ = 'down'
    _LEFT_ = 'left'
    _RIGHT_ = 'right'

    def __init__(self, color, position, line_style, text_style, show_axle=False):
        self.color = color
        self.position = position
        self.line_style = line_style
        self.text_style = text_style
        self.showAxle = show_axle


class SVGChart():

    def __init__(self, filename, profile, size, margin=(0, 0, 0, 0)):
        self.dwg = svgwrite.Drawing(filename, profile=profile, size=size)
        self.size = size
        self.filename = filename
        self.margin = margin

    def draw_background(self, background_color):
        dwg = self.dwg
        bkg_grp = dwg.g(class_='background', id='background_base')
        bkg_grp.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), id='background_rect',
                             fill=background_color))
        self.dwg.add(bkg_grp)

    def draw_axle(self, max_value, axle_style):
        raise NotImplementedError("Please Implement this method")

    def draw_data(self, data):
        raise NotImplementedError("Please Implement this method")

    def save(self):
        self.dwg.save()