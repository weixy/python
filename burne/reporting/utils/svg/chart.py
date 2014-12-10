#!/usr/bin/env python
__author__ = 'j1mw3i'
import svgwrite

UP_ = 0
DOWN_ = 1
LEFT_ = 2
RIGHT_ = 3
WIDTH_ = 0
HEIGHT_ = 1


# return the axle title point, axle title transform
def get_axle_title_style(axle_position, axle_start_p, axle_end_p):
    axle_title_styles = [
        {'offset': (0, -25), 'rotate': '0'},
        {'offset': (0, 30), 'rotate': '0'},
        {'offset': (-30, 0), 'rotate': '270'},
        {'offset': (30, 0), 'rotate': '90'},
    ]
    p1 = (axle_start_p, axle_end_p)
    offset = axle_title_styles[axle_position]['offset']
    rotate = axle_title_styles[axle_position]['rotate']
    axle_middle_p = tuple(map(lambda y: sum(y) / float(len(y)), zip(*p1)))
    p2 = (offset, axle_middle_p)
    axle_title_p = tuple(map(sum, zip(*p2)))
    axle_title_transform = 'rotate(' + rotate + ', ' + \
                           ', '.join(map(str, axle_title_p)) + ')'
    return axle_title_p, axle_title_transform


# return the gradation point, gradation end point, gradation number point and gradation line point
def get_gradation(axle_zero_point, gradation_pixel, axle_position, chart_size):
    gradation_offset = [
        {
            'gradation_point': (1, 0),
            'gradation_end_point': (0, 7),
            'number_insert_point': (0, -10),
            'gradation_line_end_point': (0, chart_size[HEIGHT_]),
        },
        {
            'gradation_point': (1, 0),
            'gradation_end_point': (0, -7),
            'number_insert_point': (0, 15),
            'gradation_line_end_point': (0, -1 * chart_size[HEIGHT_]),
        },
        {
            'gradation_point': (0, -1),
            'gradation_end_point': (7, 0),
            'number_insert_point': (-15, 0),
            'gradation_line_end_point': (chart_size[WIDTH_], 0),
        },
        {
            'gradation_point': (0, -1),
            'gradation_end_point': (-7, 0),
            'number_insert_point': (15, 0),
            'gradation_line_end_point': (-1 * chart_size[WIDTH_], 0),
        },
    ]
    grd = gradation_offset[axle_position]
    grd_point = grd['gradation_point']
    point = (
        axle_zero_point[0] + grd_point[0] * gradation_pixel,
        axle_zero_point[1] + grd_point[1] * gradation_pixel
    )
    grd_end_point = grd['gradation_end_point']
    num_ins_point = grd['number_insert_point']
    grd_lin_end_point = grd['gradation_line_end_point']
    return \
        point, \
        tuple(map(sum, zip(*(point, grd_end_point)))), \
        tuple(map(sum, zip(*(point, num_ins_point)))), \
        tuple(map(sum, zip(*(point, grd_lin_end_point))))


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

    def __init__(self, color, position, line_style, text_style, title_style,
                 show_line=True, show_number=True, show_gradation=True, show_title=True, show_gradation_line=False):
        self.color = color
        self.position = position
        self.line_style = line_style
        self.text_style = text_style
        self.title_style = title_style
        self.show_line = show_line
        self.show_gradation = show_gradation
        self.show_gradation_line = show_gradation_line
        self.show_number = show_number
        self.show_title = show_title


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
                grd_p, end_p, num_p, grd_line_p = get_gradation(
                    start_position, i * pix_gradation, axs.position, self.size
                )
                if axs.show_gradation:
                    axl_grp.add(dwg.line(start=grd_p, end=end_p, stroke=axs.color, style=axs.line_style))
                if axs.show_number:
                    axl_grp.add(dwg.text(0 + i * increment_gradation, insert=num_p, style=axs.text_style))
                if axs.show_gradation_line:
                    axl_grp.add(dwg.line(start=grd_p, end=grd_line_p, stroke=axs.color, style=axs.line_style))
        if axs.show_title:
            axl_title_p, axl_title_t = get_axle_title_style(axs.position, start_position, end_position)
            axl_grp.add(dwg.text(title, insert=axl_title_p, stroke=axs.color,
                                 transform=axl_title_t, style=axs.title_style))
        dwg.add(axl_grp)

    def draw_data(self, data):
        raise NotImplementedError("Please Implement this method")

    def save(self):
        self.dwg.save()