__author__ = 'weixy'

import os
import svgwrite


def extract_csv(file_name):
    with open(file_name) as f:
        content = f.readlines()
    lines = []
    for line in content:
        l = line.split(',')
        lines.append(tuple(float(x) if '.' in x else int(x) for x in l))
    return lines


def csv_json(file_name):
    with open(file_name) as f:
        content = f.readlines()
    report_json = {}
    lines = []
    for line in content:
        l = line.split(',')
        str_dict = {'time': l[0],
                    'ave_rsp': l[1],
                    'ave_min': l[2],
                    'ave_max': l[3],
                    'con_cur': l[4],
                    }
        lines.append(str_dict)
    report_json['data'] = lines
    return report_json


def parse_json():
    pass


def draw_svg_json(data):
    print data
    pass


def draw_svg_csv(data):
    print data
    svg_margin_x = 150
    svg_margin_y = 50
    svg_width = 1000
    svg_height = 400

    max_x = len(data)
    num_x = max_x / 10 + 1
    step_x = svg_width / num_x

    dwg = svgwrite.Drawing('load_report.svg', profile='full')
    grp_bkgrnd = dwg.g(id='background')
    grp_bkgrnd.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='#83ACEC'))

    grp_grid = dwg.g(id='g_grid')
    grp_data = dwg.g(id='g_data')
    # Draw x axle
    for i in range(num_x + 1):
        if i != 0 and i != num_x:
            grp_grid.add(dwg.line(start=(svg_margin_x + step_x * i, svg_height + svg_margin_y),
                                  end=(svg_margin_x + step_x * i, svg_margin_y),
                                  style='stroke: black; stroke-dasharray: 1 2; stroke-width: 1;'))
        grp_grid.add(dwg.text(0 + 10 * i, fill='darkgray',
                              insert=(svg_margin_x + step_x * i, svg_height + svg_margin_y + 15),
                              style='font-family: Arial; font-size: 11px; kerning: 1; text-anchor: middle;'))
    # Draw y-axle and line for each statistics
    times = [d[0] for d in data]
    max_l = [d[3] for d in data]

    for i in range(1, 5):
        l = [d[i] for d in data]
        max_y = round(max(l if i == 4 else max_l) * 1.1)
        num_y = 5
        step_y = round(svg_height / num_y)
        margin_x = 0
        left_y = 1
        axle_y_text = ''
        color = ''
        angle = '0'
        if i == 4:
            margin_x = svg_margin_x
            axle_y_text = 'Current Threads'
            color = 'rgb(0, 147, 255)'
            angle = '270'
        elif i == 1:
            margin_x = svg_margin_x + svg_width + svg_margin_x / 6
            axle_y_text = 'Average Response Time (Sec)'
            color = 'rgb(78, 165, 41)'
            angle = '90'
            left_y = -1
        elif i == 2:
            margin_x = svg_margin_x + svg_width + svg_margin_x / 3
            axle_y_text = 'Minimum Response Time (Sec)'
            color = 'rgb(127, 190, 251)'
            angle = '90'
            left_y = -1
        elif i == 3:
            margin_x = svg_margin_x + svg_width
            axle_y_text = 'Maximum Response Time (Sec)'
            color = 'rgb(242, 62, 12)'
            angle = '90'
            left_y = -1
        # Draw y axle
        if i == 4 or i == 3:
            for j in range(num_y + 1):
                grp_grid.add(dwg.line(start=(margin_x - left_y * 10, svg_height + svg_margin_y - step_y * j),
                                      end=(margin_x, svg_height + svg_margin_y - step_y * j),
                                      style='stroke: black; stroke-dasharray: 1 2; stroke-width: 1;'))
                grp_grid.add(dwg.text(int(0 + max_y / 5 * j), fill='darkgray',
                                      insert=(margin_x - left_y * 20, svg_height + svg_margin_y - step_y * j + 3),
                                      style='font-family: Arial; font-size: 11px; kerning: 1; text-anchor: middle;'))
        grp_grid.add(dwg.text(axle_y_text, fill=color,
                              insert=(margin_x - left_y * 30, svg_height / 2 + svg_margin_y),
                              transform='rotate(' + angle + ', '
                                        + str(margin_x - left_y * 30 - 10 * left_y)
                                        + ', ' + str(svg_height / 2 + svg_margin_y) + ')',
                              style='font-family: Arial; font-size: 12px; kerning: 1; text-anchor: middle;'
                              ))
        # Draw data
        points = []
        p = 0
        for time in times:
            points.append((
                svg_margin_x + round(time * (svg_width / max_x)),
                svg_height + svg_margin_y - round(l[p] * (svg_height / max_y))))
            p += 1
        print points
        grp_data.add(dwg.polyline(points, fill='none', stroke=color,
                                  style='stroke-dasharray:5 4; stroke-width:3; stroke-linecap:round;'))

    # dwg.add(grp_bkgrnd)
    dwg.add(grp_grid)
    dwg.add(grp_data)
    dwg.save()


def main():
    # json_data = csv_json('sample_data.csv')
    csv_data = extract_csv('sample_data.csv')
    draw_svg_csv(csv_data)


if __name__ == '__main__':
    main()