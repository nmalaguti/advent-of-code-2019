from __future__ import annotations

import asyncio
import fileinput
from collections import defaultdict
from enum import Enum, auto
from operator import itemgetter
from pprint import pprint
from typing import Tuple

from intcode import intcode_computer


class Direction(Enum):
    Up = auto()
    Right = auto()
    Down = auto()
    Left = auto()

    def update(self, x: int, y: int) -> Tuple[int, int]:
        if self is Direction.Up:
            return x, y - 1
        elif self is Direction.Right:
            return x + 1, y
        elif self is Direction.Down:
            return x, y + 1
        elif self is Direction.Left:
            return x - 1, y

    def turn_left(self) -> Direction:
        if self is Direction.Up:
            return Direction.Left
        elif self is Direction.Right:
            return Direction.Up
        elif self is Direction.Down:
            return Direction.Right
        elif self is Direction.Left:
            return Direction.Down

    def turn_right(self) -> Direction:
        if self is Direction.Up:
            return Direction.Right
        elif self is Direction.Right:
            return Direction.Down
        elif self is Direction.Down:
            return Direction.Left
        elif self is Direction.Left:
            return Direction.Up


if __name__ == "__main__":
    data = list(map(int, list(fileinput.input(files=["input"]))[0].split(",")))

    async def main(starting_color):
        input = asyncio.Queue()
        output = asyncio.Queue()

        hull = defaultdict(lambda: 0)
        hull[(0, 0)] = starting_color

        async def paint():
            x = y = 0
            direction = Direction.Up

            while True:
                input.put_nowait(hull[(x, y)])
                hull[(x, y)] = await output.get()
                if await output.get() == 0:
                    direction = direction.turn_left()
                else:
                    direction = direction.turn_right()

                x, y = direction.update(x, y)

        asyncio.create_task(paint())
        await asyncio.create_task(intcode_computer(data, input, output))

        return hull

    result = asyncio.run(main(0))
    pprint(len(result))

    result = asyncio.run(main(1))
    max_x = max(result.keys(), key=itemgetter(0))[0] + 1
    max_y = max(result.keys(), key=itemgetter(1))[1] + 1
    rows = list(map(list, [[" "] * max_x] * max_y))
    for (x, y), color in result.items():
        rows[y][x] = "*" if color == 1 else " "

    for row in rows:
        print("".join(row))
