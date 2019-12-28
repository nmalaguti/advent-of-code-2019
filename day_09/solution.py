from __future__ import annotations

import fileinput
from pprint import pprint

from intcode import simple

if __name__ == "__main__":
    data = list(map(int, list(fileinput.input(files=["input"]))[0].split(",")))

    pprint(simple(data, 1)[0])
    pprint(simple(data, 2)[0])
