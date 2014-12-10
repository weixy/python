#!/usr/bin/env python
__author__ = 'j1mw3i'
import svgwrite

UP_ = 0
DOWN_ = 1
LEFT_ = 2
RIGHT_ = 3
WIDTH_ = 0
HEIGHT_ = 1


class AxleStyle():

    def __init__(self, color, position,
                 line_style, text_style, show_line=True, show_number=True,
                 show_gradation=True, show_gradation_line=False):
        self.color = color
        self.position = position
        self.line_style = line_style
        self.text_style = text_style
        self.show_line = show_line
        self.show_gradation = show_gradation
        self.show_gradation_line = show_gradation_line
        self.show_number = show_number


class SVGChart():

    def __init__(self, filename, size, margin=(0, 0, 0, 0), profile='full'):
        self.dwg = svgwrite.Drawing(filename, profile=profile, size=size)
        self.size = size
        self.filename = filename
        self.margin = margin

    def draw_background(self, background_color):
        dwg = self.dwg
        bkg_grp = dwg.g(class_='background', id='background_base')
        bkg_grp.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), id='background_rect',
                             fill=background_color))
        dwg.add(bkg_grp)

    def draw_axle(self, title, max_gradation, increment_gradation, axle_style):
        dwg = self.dwg
        axl_grp = dwg.g(class_='axle')
        axl_grp.set_desc(desc=title)
        axs = axle_style
        if axs.position == UP_:
            start_position = (self.margin[LEFT_], self.margin[UP_])
            end_position = (self.size[WIDTH_] - self.margin[RIGHT_], self.margin[UP_])
            axle_length = self.size[WIDTH_] - self.margin[LEFT_] - self.margin[RIGHT_]
        elif axs.position == DOWN_:
            start_position = (self.margin[LEFT_], self.size[HEIGHT_] - self.margin[DOWN_])
            end_position = (self.size[WIDTH_] - self.margin[RIGHT_], self.size[HEIGHT_] - self.margin[DOWN_])
            axle_length = self.size[WIDTH_] - self.margin[LEFT_] - self.margin[RIGHT_]
        elif axs.position == LEFT_:
            start_position = (self.margin[LEFT_], self.size[HEIGHT_] - self.margin[DOWN_])
            end_position = (self.margin[LEFT_], self.margin[UP_])
            axle_length = self.size[HEIGHT_] - self.margin[UP_] - self.margin[DOWN_]
        elif axs.position == RIGHT_:
            start_position = (self.size[WIDTH_] - self.margin[RIGHT_], self.size[HEIGHT_] - self.margin[DOWN_])
            end_position = (self.size[WIDTH_] - self.margin[RIGHT_], self.margin[UP_])
            axle_length = self.size[HEIGHT_] - self.margin[UP_] - self.margin[DOWN_]
        else:
            raise ValueError("Incorrect position definition in axle style (0-3): '%s'" % axs.position)
        num_gradation = max_gradation / increment_gradation
        if axs.show_line:
            axl_grp.add(dwg.line(start=start_position, end=end_position,
                                 stroke=axs.color, style=axs.line_style))
        if axs.show_gradation or axs.show_number:
            for i in range(num_gradation):
                if axs.show_gradation:
                    pass
                if axs.show_number:
                    pass

        dwg.add(axl_grp)

    def draw_data(self, data):
        raise NotImplementedError("Please Implement this method")

    def save(self):
        self.dwg.save()