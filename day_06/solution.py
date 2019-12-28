import fileinput
from collections import defaultdict
from typing import Dict, Set

from sdag2 import DAG

if __name__ == "__main__":
    orbits = []
    for line in fileinput.input(files=["input"]):
        orbits.append(tuple(line.strip().split(")")))

    orbit_data: Dict[str, Set[str]] = defaultdict(set)
    rev_orbit_data: Dict[str, str] = {}
    orbit_counts: Dict[str, int] = defaultdict(lambda: 0)

    dag = DAG()

    for a, b in orbits:
        orbit_data[a].add(b)
        orbit_data[b].add(a)
        dag.add_edge(b, a)
        rev_orbit_data[b] = a

    for p in dag.topologicaly():
        try:
            orbit_counts[rev_orbit_data[p]] += orbit_counts[p] + 1
        except KeyError:
            pass

    print(sum(orbit_counts.values()))

    seen = set()

    def dfs(node, path):
        if node == "SAN":
            print(len(path) - 2)
        for v in orbit_data[node]:
            if v in seen:
                continue
            seen.add(v)
            dfs(v, path + [v])

    dfs("YOU", [])
