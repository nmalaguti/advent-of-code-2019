import fileinput
from collections import Counter
from itertools import chain
from operator import itemgetter
from pprint import pprint

if __name__ == "__main__":
    width = 25
    height = 6

    data = list(map(int, list(fileinput.input(files=["input"]))[0].strip()))

    layers = []
    layer = []
    row = []

    for pixel in data:
        row.append(pixel)
        if len(row) == width:
            layer.append(row)
            row = []
            if len(layer) == height:
                layers.append(layer)
                layer = []

    assert not layer
    assert not row

    counters = []

    for layer in layers:
        counter = Counter(chain(*layer))
        counters.append(counter)

    best_counter = sorted(counters, key=itemgetter(0))[0]
    pprint(best_counter[1] * best_counter[2])

    final_layer = list(map(list, [[9] * 25] * 6))
    for y in range(6):
        for x in range(25):
            for layer in layers:
                pixel = layer[y][x]
                if pixel != 2:
                    final_layer[y][x] = pixel
                    break

    for row in final_layer:
        print("".join("*" if x == 1 else " " for x in row))
