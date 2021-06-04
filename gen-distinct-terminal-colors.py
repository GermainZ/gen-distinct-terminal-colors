#!/usr/bin/env python
#
# Description:
# gen-distinct-terminal-colors is a simple script made to select a list of
# terminal colors that are sufficiently visually distinct. This can be useful
# for e.g. setting your IRC client's nickname colors.
#
# Syntax:
#     python gen-distinct-terminal-colors.py <output size>
#
# License:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sys import stdout, argv
from colorsys import rgb_to_hsv

from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
import numpy
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from termcolors.color_display import ColorDisplay
import wcag_contrast_ratio


# Lazy shortcut
class Container:
    pass


def main():
    palette = []
    term_colors = []
    with ColorDisplay(0, 100, 0) as C:
        # Remove colors that lack contrast with the background, to avoid
        # unreadable (dark-on-dark) choices.
        bg_color = C.get_bg()
        bg_color = (bg_color.r, bg_color.g, bg_color.b)
        for i in range(0, 230):
            color = C.get_indexed_color(i)
            term_colors.append(color)
            contrast = wcag_contrast_ratio.rgb(bg_color,
                                               (color.r, color.g, color.b))
            # "2.9" was arbitrarily chosen based on my terminal's colors'
            # contrast ratios.
            if contrast > 2.9:
                rgb = sRGBColor(color.r, color.g, color.b)
                lab = convert_color(rgb, LabColor)
                palette.append([lab.lab_l, lab.lab_a, lab.lab_b, i])
    palette = numpy.array(palette)
    n = int(argv[1])
    # Use k-means clustering to get the required amount of clusters.
    est = KMeans(n_clusters=n)
    est.fit(palette[:, 0:2])
    # Pick the closest point to each cluster's center.
    closest, _ = pairwise_distances_argmin_min(
        est.cluster_centers_, palette[:, 0:2])
    # Sort the colors using the HSV colorspace.
    sorted_colors = []
    for col in palette[closest]:
        index = col[3].astype(int)
        color = term_colors[index]
        lab = LabColor(col[0], col[1], col[2])
        c = Container()
        c.index = index
        c.sorting_key = rgb_to_hsv(*color[0:3])
        sorted_colors.append(c)
    sorted_colors.sort(key=lambda x: x.sorting_key, reverse=True)
    # Print the list of selected colors
    print(','.join([str(color.index) for color in sorted_colors]))
    # Display the sorted colors as a band
    with ColorDisplay(0, 100, 3) as C:
        for color in sorted_colors:
            index = color.index
            stdout.write(C.block(index, 3))
            stdout.write(C.fgcolor(index))
            stdout.write(' Lorem ipsum dolor sit amet\n')


if __name__ == '__main__':
    main()
