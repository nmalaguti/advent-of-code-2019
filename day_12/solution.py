import fileinput
from copy import deepcopy
from dataclasses import dataclass
from itertools import combinations, count
from math import gcd
from typing import List


@dataclass
class Moon:
    x: int
    y: int
    z: int

    vel_x: int = 0
    vel_y: int = 0
    vel_z: int = 0

    @property
    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self):
        return abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


def tick(moons: List[Moon]):
    for moon1, moon2 in combinations(moons, 2):
        if moon1.x > moon2.x:
            moon1.vel_x -= 1
            moon2.vel_x += 1
        elif moon1.x < moon2.x:
            moon1.vel_x += 1
            moon2.vel_x -= 1

        if moon1.y > moon2.y:
            moon1.vel_y -= 1
            moon2.vel_y += 1
        elif moon1.y < moon2.y:
            moon1.vel_y += 1
            moon2.vel_y -= 1

        if moon1.z > moon2.z:
            moon1.vel_z -= 1
            moon2.vel_z += 1
        elif moon1.z < moon2.z:
            moon1.vel_z += 1
            moon2.vel_z -= 1

    for moon in moons:
        moon.x += moon.vel_x
        moon.y += moon.vel_y
        moon.z += moon.vel_z


def lcm(*args):
    z = args[0]
    for i in args[1:]:
        z = z * i // gcd(z, i)
    return z


if __name__ == "__main__":
    data = []
    for line in fileinput.input(files=["input"]):
        coords = line.strip().strip("<>").split(", ")
        entry = {}
        for coord in coords:
            name, value = coord.split("=")
            entry[name] = int(value)
        data.append(Moon(**entry))

    def part1(moons):
        moons = deepcopy(moons)
        for _ in range(1000):
            tick(moons)
        return sum(m.total_energy for m in moons)

    print(part1(data))

    def find_loop(moons, axis):
        moons = deepcopy(moons)
        seen = set()
        vel = f"vel_{axis}"

        for i in count():
            all_axis = tuple((getattr(m, axis), getattr(m, vel)) for m in moons)
            if all_axis in seen:
                return i
            seen.add(all_axis)
            tick(moons)

    print(lcm(find_loop(data, "x"), find_loop(data, "y"), find_loop(data, "z")))
