#!/usr/bin/env python
__author__ = 'j1mw3i'
import svgwrite

UP_ = 0
DOWN_ = 1
LEFT_ = 2
RIGHT_ = 3
WIDTH_ = 0
HEIGHT_ = 1


def get_gradation(point, axle_position, chart_size):
    gradation = [
        {
            'gradation_end_point': (0, 7),
            'number_insert_point': (0, -10),
            'gradation_line_end_point': (0, chart_size[HEIGHT_]),
        },
        {
            'gradation_end_point': (0, -7),
            'number_insert_point': (0, 15),
            'gradation_line_end_point': (0, -1 * chart_size[HEIGHT_]),
        },
        {
            'gradation_end_point': (0, 7),
            'number_insert_point': (0, -15),
            'gradation_line_end_point': (chart_size[WIDTH_], 0),
        },
        {
            'gradation_end_point': (0, -7),
            'number_insert_point': (0, 15),
            'gradation_line_end_point': (-1 * chart_size[WIDTH_], 0),
        },
    ]
    pass


# return axle's start point, end point and length
def calculate_axle(axle_position, chart_size, chart_margin):
    if axle_position == UP_:
        start_position = (chart_margin[LEFT_], chart_margin[UP_])
        end_position = (chart_size[WIDTH_] - chart_margin[RIGHT_], chart_margin[UP_])
        axle_length = chart_size[WIDTH_] - chart_margin[LEFT_] - chart_margin[RIGHT_]
    elif axle_position == DOWN_:
        start_position = (chart_margin[LEFT_], chart_size[HEIGHT_] - chart_margin[DOWN_])
        end_position = (chart_size[WIDTH_] - chart_margin[RIGHT_], chart_size[HEIGHT_] - chart_margin[DOWN_])
        axle_length = chart_size[WIDTH_] - chart_margin[LEFT_] - chart_margin[RIGHT_]
    elif axle_position == LEFT_:
        start_position = (chart_margin[LEFT_], chart_size[HEIGHT_] - chart_margin[DOWN_])
        end_position = (chart_margin[LEFT_], chart_margin[UP_])
        axle_length = chart_size[HEIGHT_] - chart_margin[UP_] - chart_margin[DOWN_]
    elif axle_position == RIGHT_:
        start_position = (chart_size[WIDTH_] - chart_margin[RIGHT_], chart_size[HEIGHT_] - chart_margin[DOWN_])
        end_position = (chart_size[WIDTH_] - chart_margin[RIGHT_], chart_margin[UP_])
        axle_length = chart_size[HEIGHT_] - chart_margin[UP_] - chart_margin[DOWN_]
    else:
        raise ValueError("Incorrect position definition in axle style (0-3): '%s'" % axle_position)
    return start_position, end_position, axle_length


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


class Gradation():

    def __init__(self, point, axle_position, chart_size):
        self.point = point
        self.axle_position = axle_position
        self.chart_size = chart_size

    def get_gradation_end_point(self):
        pass

    def get_number_insert_point(self):
        pass

    def get_gradation_line_end_point(self):
        pass


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

        start_position, end_position, axle_length = calculate_axle(axs.position, self.size, self.margin)
        num_gradation = max_gradation / increment_gradation
        pix_gradation = float(axle_length) / num_gradation
        if axs.show_line:
            axl_grp.add(dwg.line(start=start_position, end=end_position,
                                 stroke=axs.color, style=axs.line_style))

        if axs.show_gradation or axs.show_number:
            for i in range(num_gradation + 1):
                gradation_x = start_position[0]
                gradation_y = start_position[1]
                end_x = 0
                end_y = 0
                num_x = 0
                num_y = 0
                end_g_x = 0
                end_g_y = 0
                if axs.position == UP_:
                    gradation_x += i * pix_gradation
                    end_x = gradation_x
                    end_y = gradation_y + 7
                    num_x = gradation_x
                    num_y = gradation_y - 10
                    end_g_x = end_x
                    end_g_y = gradation_y + self.size[HEIGHT_]
                elif axs.position == DOWN_:
                    gradation_x += i * pix_gradation
                    end_x = gradation_x
                    end_y = gradation_y - 7
                    num_x = gradation_x
                    num_y = gradation_y + 15
                    end_g_x = end_x
                    end_g_y = gradation_y - self.size[HEIGHT_]
                elif axs.position == LEFT_:
                    gradation_y -= i * pix_gradation
                    end_x = gradation_x + 7
                    end_y = gradation_y
                    num_x = gradation_x - 15
                    num_y = gradation_y
                    end_g_x = end_x + self.size[WIDTH_]
                    end_g_y = gradation_y
                elif axs.position == RIGHT_:
                    gradation_y -= i * pix_gradation
                    end_x = gradation_x - 7
                    end_y = gradation_y
                    num_x = gradation_x + 15
                    num_y = gradation_y
                    end_g_x = end_x - self.size[WIDTH_]
                    end_g_y = gradation_y

                if axs.show_gradation:
                    axl_grp.add(dwg.line(start=(gradation_x, gradation_y),
                                         end=(end_x, end_y),
                                         stroke=axs.color, style=axs.line_style))
                if axs.show_number:
                    axl_grp.add(dwg.text(0 + i * increment_gradation,
                                         insert=(num_x, num_y),
                                         style=axs.text_style))
                if axs.show_gradation_line:
                    axl_grp.add(dwg.line(start=(gradation_x, gradation_y),
                                         end=(end_g_x, end_g_y),
                                         stroke=axs.color, style=axs.line_style))
        dwg.add(axl_grp)

    def draw_data(self, data):
        raise NotImplementedError("Please Implement this method")

    def save(self):
        self.dwg.save()