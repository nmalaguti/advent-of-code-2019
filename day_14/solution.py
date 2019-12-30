import fileinput
import math
from collections import defaultdict, deque
from pprint import pprint

if __name__ == "__main__":
    recipes = {}
    for line in fileinput.input(files=["input"]):
        inputs = []
        recipe, result = line.split("=>")
        for component in recipe.split(","):
            amount, ingredient = component.strip().split()
            amount = int(amount)
            inputs.append((ingredient, amount))
        amount, output = result.strip().split()
        amount = int(amount)
        recipes[output] = (inputs, (output, amount))

    def reduce_to_ore(fuel, leftovers=None):
        if leftovers is None:
            leftovers = defaultdict(int)

        total_ore = 0

        queue = deque([("FUEL", fuel)])

        while queue:
            to_make, amount = queue.popleft()
            if to_make == "ORE":
                total_ore += amount
                continue

            taken = min(leftovers[to_make], amount)
            amount -= taken
            leftovers[to_make] -= taken

            if not amount:
                continue

            inputs, outputs = recipes[to_make]
            times = math.ceil(amount / outputs[1])

            leftovers[outputs[0]] += times * outputs[1] - amount

            for x, y in inputs:
                queue.append((x, y * times))

        return total_ore, leftovers

    ore_for_fuel, _ = reduce_to_ore(1)
    pprint(ore_for_fuel)

    all_ore = 1_000_000_000_000
    fuels = 0
    leftovers = defaultdict(int)
    while all_ore > 0:
        to_make = max(1, all_ore // ore_for_fuel)
        total_ore, leftovers = reduce_to_ore(to_make, leftovers)
        all_ore -= total_ore
        if all_ore > 0:
            fuels += to_make

    pprint(fuels)
