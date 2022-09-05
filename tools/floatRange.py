# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    floatRange.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/09/05 15:45:46 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/05 15:53:50 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class FloatRange:
    def __init__(self, start: int, end: int, delta: float = 1) -> None:
        self.start = start - delta
        self.end = end
        if delta == 0:
            raise ValueError("Delta cannot be zero.")
        self.delta = delta
        
    def __iter__(self) -> float:
        return self

    def __next__(self) -> float:
        self.start += self.delta
        if  self.delta > 0 and self.start >= self.end or\
            self.delta < 0 and self.start <= self.end:
            raise StopIteration
        return self.start


if __name__ == "__main__":
    print([i for i in FloatRange(0, 10, 0.5)])
    print([i for i in FloatRange(10, 0, -0.5)])
    print([i for i in FloatRange(0, 10, 1)])
    print([i for i in FloatRange(10, 0, -1)])
    print([i for i in FloatRange(0, 10, 2)])
    print([i for i in FloatRange(10, 0, -2)])
    print([i for i in FloatRange(0, 10, 3)])
    print([i for i in FloatRange(10, 0, -3)])