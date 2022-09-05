# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    .test.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/09/04 22:44:46 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/05 18:49:33 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from asciigraph import AsciiGraph
from random import randint

from tools.floatRange import FloatRange

if __name__ == "__main__":
	N = 10 + 1
	COLORS = [None, AsciiGraph.COLORS["GREEN"], AsciiGraph.COLORS["BLUE"], AsciiGraph.COLORS["YELLOW"]]
	M = len(COLORS)
	STEP = 3
	plots = []
	keys = [i + 10 for i in range(N)]
	for p in range(M):
		values = [42 + randint(-STEP * 2, STEP * 2)]
		for i in range(N - 1):
			values.append(values[-1] + randint(-STEP, STEP))

		plot = {"values": values}
		if COLORS[p] is not None:
			plot["color"] = COLORS[p]
		plots.append(plot)

	for dy in FloatRange(0.5, 1.5, 0.5, False):
		for dx in range(1, 5 + 1, 2):
			print()
			print(AsciiGraph.plot(plots, keys, dx=dx, dy=dy, hide_horizontal_axis=False))
