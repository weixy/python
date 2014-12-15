#!/usr/bin/env python
__author__ = 'j1mw3i'
import svgwrite

TOP_ = 0
BOTTOM_ = 1
LEFT_ = 2
RIGHT_ = 3
WIDTH_ = 0
HEIGHT_ = 1


class Axle():

    def __init__(self, axle_title, axle_style, gradation_max, gradation_increment):
        self.title = axle_title
        self.style = axle_style
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.gradation_max = gradation_max
        self.gradation_increment = gradation_increment

    # return axle's start point, end point and length
    def calculate_axle(self, data_view):
        position = self.style.position
        if position == TOP_:
            start_position = data_view.top_left_point
            end_position = (data_view.x + data_view.width, data_view.y)
            axle_length = data_view.width
        elif position == BOTTOM_:
            start_position = (data_view.x, data_view.y + data_view.height)
            end_position = (data_view.x + data_view.width, data_view.y + data_view.height)
            axle_length = data_view.width
        elif position == LEFT_:
            start_position = (data_view.x, data_view.y + data_view.height)
            end_position = data_view.top_left_point
            axle_length = data_view.height
        elif position == RIGHT_:
            start_position = (data_view.x + data_view.width, data_view.y + data_view.height)
            end_position = (data_view.x + data_view.width, data_view.y)
            axle_length = data_view.height
        else:
            raise ValueError("Incorrect position definition in axle style (0-3): '%s'" % position)
        return start_position, end_position, axle_length

    # return the axle title point, axle title transform
    def get_axle_title_transform(self):
        axle_title_styles = [
            {'offset': (0, -25), 'rotate': '0'},
            {'offset': (0, 30), 'rotate': '0'},
            {'offset': (-30, 0), 'rotate': '270'},
            {'offset': (30, 0), 'rotate': '90'},
        ]
        p1 = (self.start_point, self.end_point)
        offset = axle_title_styles[self.style.position]['offset']
        rotate = axle_title_styles[self.style.position]['rotate']
        axle_middle_p = tuple(map(lambda y: sum(y) / float(len(y)), zip(*p1)))
        p2 = (offset, axle_middle_p)
        axle_title_p = tuple(map(sum, zip(*p2)))
        axle_title_transform = 'rotate(' + rotate + ', ' + \
                               ', '.join(map(str, axle_title_p)) + ')'
        return axle_title_p, axle_title_transform

    # return the gradation point, gradation end point, gradation number point and gradation line point
    def get_gradation(self, gradation_pixel, data_view):
        gradation_offset = [
            {
                'gradation_point': (1, 0),
                'gradation_end_point': (0, 7),
                'number_insert_point': (0, -10),
                'gradation_line_end_point': (0, data_view.height),
            },
            {
                'gradation_point': (1, 0),
                'gradation_end_point': (0, -7),
                'number_insert_point': (0, 15),
                'gradation_line_end_point': (0, -1 * data_view.height),
            },
            {
                'gradation_point': (0, -1),
                'gradation_end_point': (5, 0),
                'number_insert_point': (-15, 0),
                'gradation_line_end_point': (data_view.width, 0),
            },
            {
                'gradation_point': (0, -1),
                'gradation_end_point': (-5, 0),
                'number_insert_point': (15, 0),
                'gradation_line_end_point': (-1 * data_view.width, 0),
            },
        ]
        grd = gradation_offset[self.style.position]
        grd_point = grd['gradation_point']
        point = (
            self.start_point[0] + grd_point[0] * gradation_pixel,
            self.start_point[1] + grd_point[1] * gradation_pixel
        )
        grd_end_point = grd['gradation_end_point']
        num_ins_point = grd['number_insert_point']
        grd_lin_end_point = grd['gradation_line_end_point']
        return \
            point, \
            tuple(map(sum, zip(*(point, grd_end_point)))), \
            tuple(map(sum, zip(*(point, num_ins_point)))), \
            tuple(map(sum, zip(*(point, grd_lin_end_point))))

    def draw(self, dwg, data_view):
        self.start_point, self.end_point, length = self.calculate_axle(data_view)
        axs = self.style
        axl_grp = dwg.g(class_='axle')
        axl_grp.set_desc(desc=self.title)
        num_gradation = self.gradation_max / self.gradation_increment
        pix_gradation = float(length) / num_gradation
        if axs.show_line:
            axl_grp.add(dwg.line(start=self.start_point, end=self.end_point,
                                 stroke=axs.color, style=axs.line_style))

        if axs.show_gradation or axs.show_number:
            for i in range(num_gradation + 1):
                grd_p, end_p, num_p, grd_line_p = self.get_gradation(i * pix_gradation, data_view)
                if axs.show_gradation:
                    axl_grp.add(dwg.line(start=grd_p, end=end_p, stroke=axs.color, style=axs.line_style))
                if axs.show_number:
                    axl_grp.add(dwg.text(0 + i * self.gradation_increment, insert=num_p, style=axs.text_style))
                if axs.show_gradation_line and i != 0 and i != num_gradation:
                    axl_grp.add(dwg.line(start=grd_p, end=grd_line_p, stroke=axs.color, style=axs.line_style))
        if axs.show_title:
            axl_title_p, axl_title_t = self.get_axle_title_transform()
            axl_grp.add(dwg.text(self.title, insert=axl_title_p, stroke=axs.color,
                                 transform=axl_title_t, style=axs.title_style))
        return axl_grp


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


class DataViewRect():

    def __init__(self, size, margin):
        self.top_left_point = (margin[LEFT_], margin[TOP_])
        self.x = margin[LEFT_]
        self.y = margin[TOP_]
        self.width = size[WIDTH_] - margin[LEFT_] - margin[RIGHT_]
        self.height = size[HEIGHT_] - margin[TOP_] - margin[BOTTOM_]


class SVGChart():

    def __init__(self, filename, size, margin=(0, 0, 0, 0), profile='full'):
        self.dwg = svgwrite.Drawing(filename, profile=profile, size=size, class_='line_chart')
        self.dwg.set_desc(title='Chart')
        self.size = size
        self.filename = filename
        self.margin = margin
        self.data_view = DataViewRect(size, margin)

    def add_background(self, background_color):
        dwg = self.dwg
        bkg_grp = dwg.g(class_='background', id='background_base')
        bkg_grp.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), id='background_rect',
                             fill=background_color))
        dwg.add(bkg_grp)

    def add_axle(self, title, max_gradation, increment_gradation, axle_style):
        dwg = self.dwg
        axle = Axle(title, axle_style, max_gradation, increment_gradation)
        axl_grp = axle.draw(dwg, self.data_view)
        dwg.add(axl_grp)
        return axle

    def add_data(self, data, color, axle_x, axle_y):
        raise NotImplementedError("Please Implement this method")

    def save(self):
        self.dwg.save()