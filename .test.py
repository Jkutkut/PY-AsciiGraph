# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    .test.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/09/04 22:44:46 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/04 22:46:03 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from asciigraph import AsciiGraph
from random import randint

if __name__ == "__main__":
	N = 10 + 1
	keys = [i + 10 for i in range(N)]
	# values1 = [randint(30, 42) for i in range(N)]
	# values2 = [randint(30, 42) for i in range(N)]
	values1 = [randint(0, 42)]
	values2 = [randint(0, 42)]
	for i in range(N - 1):
		values1.append(values1[-1] + randint(-5, 5))
		values2.append(values2[-1] + randint(-5, 5))
	print(AsciiGraph.plot([{"values": values1}, {"values": values2, "color": AsciiGraph.COLORS["GREEN"]}], keys))
	print()
	print(AsciiGraph.plot([{"values": values1}, {"values": values2, "color": AsciiGraph.COLORS["GREEN"]}], keys, dx = 3))
	print()
	print(AsciiGraph.plot([{"values": values1}, {"values": values2, "color": AsciiGraph.COLORS["GREEN"]}], keys, dx = 5))
	print()
