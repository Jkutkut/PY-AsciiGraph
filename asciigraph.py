# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    asciigraph.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/08/04 15:03:53 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/04 22:45:11 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import math

class AsciiGraph:
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

	@classmethod
	def plot(cls, plots: list, keys: list, dy: int = 1, dx: int = 1, min_value_overlap_axis: bool = False, hide_horizontal_axis: bool = True) -> str:
		t = len(keys)

		if any([len(k["values"]) != t for k in plots]):
			raise Exception("Inconsistent data")
		if dx < 1:
			raise Exception("Invalid dx")


		mini = min([min(p["values"]) for p in plots])
		maxi = max([max(p["values"]) for p in plots])
		Y = (maxi - mini + 1) // dy

		mapa = [list("".ljust(t * dx)) for _ in range(Y)]

		# Fill plot
		for plot in plots:
			values = plot["values"]
			color = cls.NC
			if "color" in plot:
				color = plot["color"]
			prev = values[0]
			for i in range(t):
				x = i * dx
				y = (maxi - values[i]) // dy

				# Connection to previous point logic
				dot = None
				connector = None
				iterator = (0, 0)
				if prev < values[i]:
					dot = cls.UP_CURVE_E
					connector = cls.UP_CURVE_S
					iterator = (prev + 1, values[i])
				elif  prev > values[i]:
					dot = cls.DOWN_CURVE_E
					connector = cls.DOWN_CURVE_S
					iterator = (values[i] + 1, prev)
				else:
					dot = cls.H_LINE

				# value representation
				mapa[y][x] = cls.DRAW(dot, color)
				if connector != None:
					y2 = (maxi - prev) // dy
					mapa[y2][x] = cls.DRAW(connector, color)
				for j in range(*iterator):
					yj = (maxi - j) // dy
					mapa[yj][x] = cls.DRAW(cls.V_LINE, color)
				
				# Horizontal spacing
				for j in range(1, dx):
					mapa[y][x + j] = cls.DRAW(cls.H_LINE, color)

				prev = values[i]

		# Y axis
		for i in range(Y):
			y_value = f"{maxi - i * dy}".center(cls.Y_SIZE)
			mapa[i] = f"{y_value}{cls.TOP_CORNER}{''.join(mapa[i])}"
		
		# X axis
		horizontal_line = " " if hide_horizontal_axis else cls.H_LINE
		xaxis = "".join(["".ljust(cls.Y_SIZE)] + [cls.DOWN_CURVE_E] + [horizontal_line for _ in range(t * dx)])
		if min_value_overlap_axis:
			mapa[-1] = xaxis
		else:
			mapa.append(xaxis)
		
		keys = [f"{k}" for k in keys] # To str list
		longest = max([len(k) for k in keys])
		if dx > longest:
			# xspace = math.ceil(longest / dx)
			# for i in range(xspace):
			# mapa.append(list("".ljust(cls.Y_SIZE + 1 + t * dx)))
			axis = []
			for i in range(t):
				k = keys[i]
				axis.append(k.center(dx))
			axis = "".ljust(cls.Y_SIZE + 1) + "".join(axis)
			mapa.append(axis)
			# for i in range(xspace):
			mapa[-1] = "".join(mapa[-1])
		
		return "\n".join(mapa)
