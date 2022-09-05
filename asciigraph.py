# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    asciigraph.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/08/04 15:03:53 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/05 16:08:40 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import math

from tools.floatRange import FloatRange

class AsciiGraph:
    '''
    Class with logic to generate plots with ascii characters.
    '''

    TOP_CORNER = "┼"
    V_LINE = "│"
    H_LINE = "─"
    UP_CURVE_S = "╯"
    UP_CURVE_E = "╭"
    DOWN_CURVE_S = "╮"
    DOWN_CURVE_E = "╰"

    Y_SIZE = 6

    X_SIZE = 5

    NC = "\033[0m"

    COLORS = {
        "RED": "\033[0;31m",
        "GREEN": "\033[0;32m",
        "BLUE": "\033[0;34m",
        "YELLOW": "\033[0;33m",
        "NC": NC
    }

    DRAW = lambda point, color : f"{color}{point}{AsciiGraph.NC}"

    # *********** DATA VALIDATION ***********
    @classmethod
    def _data_validation(cls, plots: list, keys: list, dy: int = 1, dx: int = 1) -> None:
        t = len(keys)
        if any([len(k["values"]) != t for k in plots]):
            raise Exception("Inconsistent data")
        if dx < 1:
            raise Exception("Invalid dx")
        if dy > 1:
            raise Exception("Invalid dy")
        # TODO dy > 1 scales graph

    @classmethod
    def _analice_values(cls, plots: list, dy: int = 1) -> dict:
        min_y = min([min(p["values"]) for p in plots])
        max_y = max([max(p["values"]) for p in plots])
        Y = int((max_y - min_y + 1) // dy)
        return (min_y, max_y, Y)

    # *********** DRAWING ***********
    @classmethod
    def _create_map(self, t: int, Y: int, dx: int) -> list:
        return [list("".ljust(t * dx)) for _ in range(Y)]

    @classmethod
    def _plot_values(cls, map: list, plot: dict, t: int, max_y: int, dx: int, dy: int):
        values = plot["values"]
        color = cls.NC
        if "color" in plot:
            color = plot["color"]
        prev = values[0]
        for i in range(t):
            x = i * dx
            y = int((max_y - values[i]) // dy)

            # Connection to previous point logic
            dot = None
            connector = None
            iterator = (0, 0)
            if prev < values[i]:
                dot = cls.UP_CURVE_E
                connector = cls.UP_CURVE_S
                iterator = (prev + dy, values[i], dy)
            elif  prev > values[i]:
                dot = cls.DOWN_CURVE_E
                connector = cls.DOWN_CURVE_S
                iterator = (values[i] + dy, prev, dy)
            else:
                dot = cls.H_LINE

            # value representation
            map[y][x] = cls.DRAW(dot, color)
            if connector != None:
                y2 = int((max_y - prev) // dy)
                map[y2][x] = cls.DRAW(connector, color)
            for j in FloatRange(*iterator):
                yj = int((max_y - j) // dy)
                map[yj][x] = cls.DRAW(cls.V_LINE, color)
            
            # Horizontal spacing
            for j in range(1, dx):
                map[y][x + j] = cls.DRAW(cls.H_LINE, color)
            prev = values[i]

    @classmethod
    def _draw_y_axis(cls, map: list, Y: int, max_y: int, dy: int) -> None:
        for i in range(Y):
            y_value = f"{max_y - i * dy}".center(cls.Y_SIZE)
            map[i] = f"{y_value}{cls.TOP_CORNER}{''.join(map[i])}"

    @classmethod
    def _draw_x_axis(cls, keys: list, map: list, t: int, dx: int, hide_horizontal_axis: bool, min_value_overlap_axis: bool) -> None:
        horizontal_line = " " if hide_horizontal_axis else cls.H_LINE
        xaxis = "".ljust(cls.Y_SIZE) + cls.DOWN_CURVE_E + "".join([horizontal_line for _ in range(t * dx)])
        # Add the axis into the map
        if min_value_overlap_axis:
            map[-1] = xaxis # Removing the last line with the axis
        else:
            map.append(xaxis)
        
        keys = [f"{k}" for k in keys] # To str list
        longest = max([len(k) for k in keys])
        if dx <= longest:
            return
        axis = []
        for i in range(t):
            k = keys[i]
            axis.append(k.center(dx))
        axis = "".ljust(cls.Y_SIZE + 1) + "".join(axis)
        map.append(axis)
        # for i in range(xspace):
        map[-1] = "".join(map[-1])

    @classmethod
    def plot(cls, plots: list, keys: list, dy: int = 1, dx: int = 1,\
            min_value_overlap_axis: bool = False,\
            hide_horizontal_axis: bool = True) -> str:
        t = len(keys)

        cls._data_validation(plots, keys, dy, dx)

        min_y, max_y, Y = cls._analice_values(plots, dy)

        mapa = cls._create_map(t, Y, dx)

        # Fill plot
        for plot in plots:
            cls._plot_values(mapa, plot, t, max_y, dx, dy)

        # X, Y axis
        cls._draw_y_axis(mapa, Y, max_y, dy)
        cls._draw_x_axis(keys, mapa, t, dx, hide_horizontal_axis, min_value_overlap_axis)
        
        return "\n".join(mapa)
