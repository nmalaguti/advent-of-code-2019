import fileinput
from copy import deepcopy
from typing import List


def run(memory: List[int]):
    memory += (4 - (len(memory) % 4)) * [0]
    for i in range(0, len(memory), 4):
        a, b, c, d = memory[i : i + 4]
        if a == 99:
            return memory[0]
        elif a == 1:
            memory[d] = memory[b] + memory[c]
        elif a == 2:
            memory[d] = memory[b] * memory[c]
        else:
            raise RuntimeError(f"Unexpected opcode {a!r}")


def main1(problem):
    problem = deepcopy(problem)
    problem[1] = 12
    problem[2] = 2
    return run(problem)


def main2(problem, target):
    for i in range(100):
        for j in range(100):
            attempt = deepcopy(problem)
            attempt[1] = i
            attempt[2] = j
            if run(attempt) == target:
                return 100 * i + j


if __name__ == "__main__":
    data = list(map(int, list(fileinput.input(files=["input"]))[0].split(",")))
    print(main1(data))
    print(main2(data, 19690720))
