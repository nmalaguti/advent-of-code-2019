from __future__ import annotations

import asyncio
import fileinput
from collections import Counter
from copy import deepcopy
from operator import itemgetter
from pprint import pprint

from blessed import Terminal
from more_itertools import grouper

from intcode import intcode_computer, simple

term = Terminal()

if __name__ == "__main__":
    data = list(map(int, list(fileinput.input(files=["input"]))[0].split(",")))

    def part1(program):
        program = deepcopy(program)
        screen = {}

        for (x, y, tile) in grouper(simple(program), 3):
            screen[(x, y)] = tile

        pprint(Counter(screen.values())[2])

    part1(data)

    async def part2(program):
        program = deepcopy(program)
        program[0] = 2

        screen = {}
        score = 0
        ball_x = 0
        paddle_x = 0
        output = asyncio.Queue()

        class Input:
            async def get(self):
                await output.join()

                if ball_x > paddle_x:
                    return 1
                if ball_x < paddle_x:
                    return -1

                return 0

        input = Input()

        async def update_screen():
            nonlocal paddle_x, ball_x, score
            while True:
                x = await output.get()
                output.task_done()
                y = await output.get()
                output.task_done()
                tile = await output.get()
                output.task_done()
                if (x, y) == (-1, 0):
                    score = tile
                if tile == 3:
                    paddle_x = x
                elif tile == 4:
                    ball_x = x

                # screen[(x, y)] = tile
                #
                # if output.empty() and screen:
                #     await asyncio.sleep(0.1)
                #     print(term.clear())
                #     print(term.move(0, 0))
                #     max_x = max(screen.keys(), key=itemgetter(0))[0] + 1
                #     max_y = max(screen.keys(), key=itemgetter(1))[1] + 1
                #     rows = list(map(list, [[" "] * max_x] * max_y))
                #     sprites = [
                #         " ",
                #         term.on_yellow(" "),
                #         term.on_red(" "),
                #         term.on_blue(" "),
                #         term.on_white(" "),
                #     ]
                #     for (x, y), tile in screen.items():
                #         if x == -1:
                #             print("Score:", tile)
                #             continue
                #         rows[y][x] = sprites[tile]
                #
                #     for row in rows:
                #         print("".join(row))
                #     print()

        asyncio.create_task(update_screen())
        await asyncio.create_task(intcode_computer(program, input, output))
        await output.join()
        pprint(score)

    asyncio.run(part2(data))
