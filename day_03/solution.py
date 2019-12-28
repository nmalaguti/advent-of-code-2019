import fileinput
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import count
from typing import Dict, List, Mapping, Set, Tuple, Union


class Direction(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


@dataclass
class PathSegment:
    direction: Direction
    distance: int

    @classmethod
    def from_str(cls, txt: str):
        return PathSegment(Direction(txt[0]), int(txt[1:]))


def path_points(
    path_segments: List[PathSegment],
) -> Tuple[Set[Tuple[int, int]], Mapping[Tuple[int, int], Union[int, float]]]:
    points = set()
    point_steps: Dict[Tuple[int, int], Union[int, float]] = defaultdict(
        lambda: float("inf")
    )
    steps = count(1)
    x = y = 0

    for path_segment in path_segments:
        for i in range(path_segment.distance):
            if path_segment.direction is Direction.Up:
                y += 1
            if path_segment.direction is Direction.Down:
                y -= 1
            if path_segment.direction is Direction.Left:
                x -= 1
            if path_segment.direction is Direction.Right:
                x += 1
            points.add((x, y))
            point_steps[(x, y)] = min(next(steps), point_steps[(x, y)])

    return points, point_steps


if __name__ == "__main__":
    wires = list(fileinput.input(files=["input"]))
    # wires = dedent(
    #     """\
    #     R75,D30,R83,U83,L12,D49,R71,U7,L72
    #     U62,R66,U55,R34,D71,R55,D58,R83
    #     """
    # ).splitlines()
    wire1_path = list(map(PathSegment.from_str, wires[0].split(",")))
    wire2_path = list(map(PathSegment.from_str, wires[1].split(",")))
    wire1_points, wire1_point_steps = path_points(wire1_path)
    wire2_points, wire2_point_steps = path_points(wire2_path)
    intersections = wire1_points.intersection(wire2_points)
    closest_point = sorted(map(lambda p: abs(p[0]) + abs(p[1]), intersections))[0]
    print(closest_point)
    shortest_steps = sorted(
        map(lambda p: wire1_point_steps[p] + wire2_point_steps[p], intersections)
    )[0]
    print(shortest_steps)
