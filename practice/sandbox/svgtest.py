__author__ = 'weixy'

import svgwrite

dwg = svgwrite.Drawing('test.svg', profile='full')
grp = dwg.g(id='background')
grp.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='#83ACEC'))

grp_grid = dwg.g(id='grid')
for i in range(5):
    grp_grid.add(dwg.line(start=(113 + 146 * i, 10), end=(113 + 146 * i, 380),
                          style='stroke: white;stroke-dasharray: 1 2;stroke-width: 1;'))
for j in range(7):
    grp_grid.add(dwg.line(start=(86, 10 + 58 * j), end=(697, 10 + 58 * j),
                          style='stroke: white;stroke-dasharray: 1 2;stroke-width: 1;'))
grp_data = dwg.g(id='data')
grp_data.add(dwg.circle(center=(113, 192), r=5,
                        style='stroke: white; stroke-width: 3;'))
grp_data.add(dwg.circle(center=(259, 171), r=5,
                        style='stroke: white; stroke-width: 3;'))
grp_data.add(dwg.circle(center=(405, 179), r=5,
                        style='stroke: white; stroke-width: 3;'))
grp_data.add(dwg.circle(center=(551, 200), r=5,
                        style='stroke: white; stroke-width: 3;'))
grp_data.add(dwg.circle(center=(697, 204), r=5,
                        style='stroke: white; stroke-width: 3;'))
grp_area = dwg.g(id='area')
grp_area.add(dwg.path(d='M113,360 L113,192 L259,171 L405,179 L551,200 L697,204 L697,360 Z',
                      style='fill: #002B55; fill-opacity: 0.5;'))
grp_area.add(dwg.use(href='#grid', style='stroke-opacity: 0.4;'))
grp_area.add(dwg.use(href='#data'))

grp_label = dwg.g(id='labels')
grp_grid.add(dwg.text('2008', insert=(113, 400),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: middle;'))
grp_grid.add(dwg.text('2009', insert=(259, 400),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: middle;'))
grp_grid.add(dwg.text('2010', insert=(405, 400),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: middle;'))
grp_grid.add(dwg.text('2011', insert=(551, 400),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: middle;'))
grp_grid.add(dwg.text('2012', insert=(697, 400),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: middle;'))

grp_grid.add(dwg.text('15', insert=(80, 15),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: end;'))
grp_grid.add(dwg.text('10', insert=(80, 131),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: end;'))
grp_grid.add(dwg.text('5', insert=(80, 248),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: end;'))
grp_grid.add(dwg.text('9', insert=(80, 365),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: end;'))
grp_grid.add(dwg.text('Weeks', insert=(50, 15),
                      style='font-family: Arial; font-size: 14px; kerning: 1; text-anchor: end;'))


# grp.add(canvas.rect(insert=(5, 5), size=(300, 500), fill='rgb(50, 50, 50)'))
#
# blur_filter = canvas.defs.add(canvas.filter())
# blur_filter.feGaussianBlur(in_='SourceGraphic', stdDeviation=6)
#
# g_f = grp.add(canvas.g(filter=blur_filter.get_funciri()))
# g_f.add(canvas.rect(insert=(20, 20), size=(80, 100), fill='aqua'))

dwg.add(grp)
dwg.add(grp_grid)
dwg.add(grp_data)
dwg.add(grp_area)
dwg.add(grp_label)
dwg.save()