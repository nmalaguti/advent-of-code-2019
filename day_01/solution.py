import fileinput


def fuel_for_module(x):
    return x // 3 - 2


def fuel_for_module_and_fuel(module):
    fuel = total = fuel_for_module(module)
    while fuel > 0:
        fuel = fuel_for_module(fuel)
        total += max(fuel, 0)
    return total


def main1(problem):
    return sum(fuel_for_module(x) for x in problem)


def main2(problem):
    return sum(fuel_for_module_and_fuel(x) for x in problem)


if __name__ == "__main__":
    data = list(map(int, fileinput.input(files=["input"])))
    print(main1(data))
    print(main2(data))
