from __future__ import annotations

import asyncio
import fileinput
from itertools import permutations
from pprint import pprint
from typing import Iterator

from intcode import intcode_computer

if __name__ == "__main__":
    data = list(map(int, list(fileinput.input(files=["input"]))[0].split(",")))

    async def run_amps(order: Iterator):
        queues = [asyncio.Queue() for _ in range(5)]

        for q, i in zip(queues, order):
            q.put_nowait(i)

        queues[0].put_nowait(0)

        tasks = [
            asyncio.create_task(intcode_computer(data, queues[i], queues[(i + 1) % 5]))
            for i in range(5)
        ]

        await asyncio.gather(*tasks)

        return queues[0].get_nowait()

    def main1():
        outputs = []

        for o in permutations(range(5)):
            outputs.append(asyncio.run(run_amps(o)))

        pprint(max(outputs))

    main1()

    def main2():
        outputs = []

        for o in permutations(range(5, 10)):
            outputs.append(asyncio.run(run_amps(o)))

        pprint(max(outputs))

    main2()
