__author__ = 'weixy'

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


def get_axle_value(v):
    d_num = len(str(v))
    d_tmp = pow(10, d_num - 1)
    axle_max = ((v / d_tmp) + 1) * d_tmp
    axle_step = pow(10, d_num - 1) / 2 if axle_max <= (pow(10, d_num) / 2) else pow(10, d_num - 1)
    axle_num = axle_max / axle_step + 1
    return axle_max, axle_step, axle_num


def draw_svg_csv(data):
    svg_margin_x = 100
    svg_margin_y = 50
    svg_width = 800
    svg_height = 300
    svg_background = 'rgb(242, 242, 242)'
    thread_color = 'rgb(0, 147, 255)'
    average_color = 'rgb(78, 165, 41)'
    maximum_color = 'rgb(242, 62, 12)'
    axle_color = 'darkgray'
    axle_line_style = 'stroke-dasharray: 1 2; stroke-width: 1;'
    axle_text_style = 'font-size: 11px; text-anchor: middle;'

    times = [d[0] for d in data]
    thd_l = [d[4] for d in data]
    max_l = [d[3] for d in data]
    ave_l = [d[1] for d in data]

    max_x = len(data)
    num_x = max_x / 10 + 1
    max_x = num_x * 10
    step_x = svg_width / num_x

    dwg = svgwrite.Drawing('load_report.svg', profile='full',
                           style='font-family: Arial; kerning: 1;')
    grp_bkgrnd = dwg.g(id='background')
    grp_bkgrnd.add(dwg.rect(insert=(0, 0),
                            size=(svg_width + svg_margin_x * 2, svg_height + svg_margin_y * 2),
                            rx=None, ry=None, fill=svg_background))

    grp_grid = dwg.g(id='g_grid', fill=axle_color)
    grp_data = dwg.g(id='g_data')
    # Draw x axle
    for i in range(0, num_x + 1):
        x = svg_margin_x + step_x * i
        if i != 0 and i != num_x:
            grp_grid.add(dwg.line(start=(x, svg_height + svg_margin_y), end=(svg_margin_x + step_x * i, svg_margin_y),
                                  stroke=axle_color, style=axle_line_style))
            grp_grid.add(dwg.text(0 + 10 * i, insert=(x, svg_height + svg_margin_y + 15),
                                  style=axle_text_style))
        else:
            grp_grid.add(dwg.line(start=(x, svg_height + svg_margin_y), end=(x, svg_height + svg_margin_y + 10),
                                  stroke=axle_color, style=axle_line_style))
            grp_grid.add(dwg.text(0 + 10 * i, insert=(x, svg_height + svg_margin_y + 15),
                                  style=axle_text_style))
    grp_grid.add(dwg.text('Time (sec)',
                          insert=(svg_width / 2 + svg_margin_x, svg_height + svg_margin_y + 35),
                          style='font-size: 13px; text-anchor: middle;'))

    # Draw y-axle
    thd_y_max, thd_y_step, thd_y_num = get_axle_value(int(max(thd_l)))
    max_y_max, max_y_step, max_y_num = get_axle_value(int(max(max_l)))
    thd_y_dist = svg_height / (thd_y_num - 1)
    for i in range(thd_y_num):
        y = svg_height + svg_margin_y - thd_y_dist * i
        grp_grid.add(dwg.line(start=(svg_margin_x, y), end=(svg_margin_x - 10, y),
                              stroke=axle_color, style=axle_line_style))
        grp_grid.add(dwg.text(i * thd_y_step, insert=(svg_margin_x - 20, y + 5),
                              fill=axle_color, style=axle_text_style))
    max_y_dist = svg_height / (max_y_num - 1)
    for i in range(max_y_num):
        y = svg_height + svg_margin_y - max_y_dist * i
        grp_grid.add(dwg.line(start=(svg_margin_x + svg_width, y), end=(svg_margin_x + svg_width + 10, y),
                              stroke=axle_color, style=axle_line_style))
        grp_grid.add(dwg.text(i * max_y_step, insert=(svg_margin_x + svg_width + 20, y + 5),
                              fill=axle_color, style=axle_text_style))

    # Draw legends
    legend_y = svg_height / 2 + svg_margin_y
    legend_style = 'font-size: 12px; text-anchor: middle;'
    grp_grid.add(dwg.text('Current Threads', fill=thread_color,
                          insert=(svg_margin_x - 40, legend_y),
                          transform='rotate(270,' + str(svg_margin_x - 40)
                                    + ', ' + str(legend_y) + ')',
                          style=legend_style
                          ))
    grp_grid.add(dwg.text('Average Response Time (Sec)', fill=average_color,
                          insert=(svg_margin_x + svg_width + 40, legend_y),
                          transform='rotate(90,' + str(svg_margin_x + svg_width + 40)
                                    + ', ' + str(legend_y) + ')',
                          style=legend_style
                          ))
    grp_grid.add(dwg.text('Maximum Response Time (Sec)', fill=maximum_color,
                          insert=(svg_margin_x + svg_width + 60, legend_y),
                          transform='rotate(90,' + str(svg_margin_x + svg_width + 60)
                                    + ', ' + str(legend_y) + ')',
                          style=legend_style
                          ))

    # Draw data
    points_thd = zip(times, thd_l)
    pixels_thd = [(svg_margin_x + round(p[0] * (float(svg_width) / max_x)),
                  svg_height + svg_margin_y - round(p[1] * (float(svg_height) / thd_y_max))) for p in points_thd]
    line = dwg.polyline(pixels_thd, fill='none', stroke=thread_color,
                              style='stroke-width:2; stroke-linecap:round;')
    line.set_desc(desc='thread')
    grp_data.add(line)

    points_ave = zip(times, ave_l)
    pixels_ave = [(svg_margin_x + round(p[0] * (float(svg_width) / max_x)),
                  svg_height + svg_margin_y - round(p[1] * (float(svg_height) / max_y_max))) for p in points_ave]
    grp_data.add(dwg.polyline(pixels_ave, fill='none', stroke=average_color,
                              style='stroke-dasharray:6 6; stroke-width:2; stroke-linecap:round;'))

    points_max = zip(times, max_l)
    pixels_max = [(svg_margin_x + round(p[0] * (float(svg_width) / max_x)),
                  svg_height + svg_margin_y - round(p[1] * (float(svg_height) / max_y_max))) for p in points_max]
    grp_data.add(dwg.polyline(pixels_max, fill='none', stroke=maximum_color,
                              style='stroke-dasharray:3 3; stroke-width:2; stroke-linecap:round;'))

    dwg.add(grp_bkgrnd)
    dwg.add(grp_grid)
    dwg.add(grp_data)
    dwg.save()


def main():
    # json_data = csv_json('sample_data.csv')
    csv_data = extract_csv('sample_data.csv')
    draw_svg_csv(csv_data)


if __name__ == '__main__':
    main()