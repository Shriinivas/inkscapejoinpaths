#!/usr/bin/env python
"""
Inkscape extension to join the selected paths

Author: Shrinivas Kulkarni (khemadeva@gmail.com)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import inkex
from inkex import PathElement, Path, Boolean
from inkex.bezier import pointdistance


class ConnectPaths(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--factor", type=float, default=0.2)
        pars.add_argument("--path_order", type=str, default="z_order")
        pars.add_argument("--subpath_handling", type=str, default="break_apart")
        pars.add_argument("--close_path", type=Boolean, default=True)
        pars.add_argument("--delete_orig", type=Boolean, default=False)
        pars.add_argument("--tab", help="Select Options")

    def effect(self):
        paths = self.svg.selection.get(PathElement)
        if len(paths) < 2:
            inkex.errormsg("Please select at least 2 paths to join.")
            return

        path_order = self.options.path_order
        subpath_handling = self.options.subpath_handling
        close_path = self.options.close_path
        delete_orig = self.options.delete_orig
        factor = self.options.factor

        ordered_paths = self.order_paths(paths, path_order, subpath_handling)
        connected_path = self.connect_paths(ordered_paths, close_path, factor)

        if close_path:
            connected_path.close()

        new_path = PathElement()
        new_path.path = connected_path
        new_path.style = paths[0].style
        self.svg.add(new_path)

        if delete_orig:
            for p in paths:
                p.getparent().remove(p)

    def order_paths(self, pathElems, order_type, subpath_handling):
        def get_paths():
            if subpath_handling == "break_apart":
                return [
                    sub.transform(p.composed_transform())
                    for p in pathElems
                    for sub in p.path.to_absolute().break_apart()
                ]
            else:
                return [
                    p.path.to_absolute().transform(p.composed_transform())
                    for p in pathElems
                ]

        if order_type in {
            "selection_order",
            "z_order",
            "selection_order_rev",
            "z_order_rev",
        }:
            if order_type == "z_order":
                pathElems = pathElems.rendering_order()
            pathElems = pathElems.values()  # for the sake of uniformity
            if order_type.endswith("_rev"):
                pathElems = reversed(pathElems)
            return get_paths()
        elif order_type == "distance":
            paths = get_paths()
            ordered = [paths[0]]
            remaining = paths[1:]
            while remaining:
                end_point = list(ordered[-1].end_points)[-1]
                cmp_paths = []
                for ppath in remaining:
                    pts = list(ppath.end_points)
                    cmp_paths.append([ppath, pts[0], True])
                    cmp_paths.append([ppath, pts[-1], False])
                nearest = min(cmp_paths, key=lambda p: pointdistance(end_point, p[1]))
                next_path = nearest[0] if nearest[2] else nearest[0].reverse()
                ordered.append(next_path)
                remaining.remove(nearest[0])
            return ordered

    def connect_paths(self, paths, close_path, factor) -> Path:
        connected = paths[0]
        connected_csp = connected.to_superpath()
        list_paths = paths[1:] + ([paths[0]] if close_path else [])
        for i, path in enumerate(list_paths):
            if factor == 0:
                if i < len(list_paths) - 1 or not close_path:
                    next_start = next(path.proxy_iterator()).first_point
                    connected.append(Path(f"L {next_start[0]},{next_start[1]}"))
                    connected.extend(path[1:])
            else:
                last_segment = connected_csp[-1][-1]
                last_endpoint = last_segment[1]
                last_ctrl_pt = last_segment[0]
                prev_point = connected_csp[-1][-2][1]
                last_segment[2] = self.find_opposite_point(
                    last_endpoint, last_ctrl_pt, prev_point, factor
                )

                next_path_csp = path.to_superpath()
                first_segment = next_path_csp[0][0]
                first_startpt = first_segment[1]
                first_ctrl_pt = first_segment[2]
                next_point = next_path_csp[0][1][1]
                first_segment[0] = self.find_opposite_point(
                    first_startpt, first_ctrl_pt, next_point, factor
                )
                if i < len(list_paths) - 1 or not close_path:
                    connected_csp[-1] += next_path_csp[0]
                else:
                    connected_csp[-1].append(next_path_csp[0][0])
        if factor != 0:
            connected = Path(connected_csp)

        return connected

    def find_opposite_point(self, p1, p2, fall_back, factor):
        factor = -factor
        if all(p1[i] == p2[i] for i in range(2)):
            p2 = fall_back
        # get point away from p1 at a factor of p2's distance from p1
        return [((1 - factor) * p1[i] + factor * p2[i]) for i in range(2)]


if __name__ == "__main__":
    ConnectPaths().run()
