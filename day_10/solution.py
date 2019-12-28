import fileinput
from collections import defaultdict
from fractions import Fraction
from pprint import pprint
from typing import Set, Tuple

if __name__ == "__main__":
    data = list(fileinput.input(files=["input"]))

    original_asteroids = set()

    for y, line in enumerate(data):
        for x, char in enumerate(line.strip()):
            if char == "#":
                original_asteroids.add((x, y))

    def main1():

        max_seen = 0, (-1, -1)

        def visible(asteroids: Set[Tuple[int, int]], source: Tuple[int, int]):
            slopes = set()
            for x, y in asteroids:
                if (x, y) == source:
                    continue

                try:
                    f = Fraction(y - source[1], x - source[0])
                except ZeroDivisionError:
                    f = float("-inf")

                if x >= source[0] and y <= source[1]:
                    quad = 0
                elif x >= source[0] and y > source[1]:
                    quad = 1
                elif x < source[0] and y >= source[1]:
                    quad = 2
                else:
                    quad = 3

                slopes.add((quad, f))

            return len(slopes)

        for asteroid in original_asteroids:
            result = visible(original_asteroids, asteroid), asteroid
            max_seen = max(max_seen, result)

        pprint(max_seen[0])
        return max_seen[1]

    best_loc = main1()

    lookup = defaultdict(list)

    for x, y in original_asteroids:
        if (x, y) == best_loc:
            continue

        try:
            f = Fraction(y - best_loc[1], x - best_loc[0])
        except ZeroDivisionError:
            f = float("-inf")

        if x >= best_loc[0] and y <= best_loc[1]:
            quad = 0
        elif x >= best_loc[0] and y > best_loc[1]:
            quad = 1
        elif x < best_loc[0] and y >= best_loc[1]:
            quad = 2
        else:
            quad = 3

        lookup[(quad, f)].append((x, y))

    destruction_order = sorted(lookup.items())
    for _, points in destruction_order:
        points.sort(key=lambda x: abs(x[0] - best_loc[0]) + abs(x[1] - best_loc[1]))

    boomed = []
    while any(p for _, p in destruction_order):
        for _, points in destruction_order:
            if points:
                boomed.append(points.pop(0))

    twohundred = boomed[199]
    pprint(twohundred[0] * 100 + twohundred[1])
