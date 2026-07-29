# Path Finder

[![ci](https://github.com/yashasviyadav30/Grid-Pathfinder/actions/workflows/ci.yml/badge.svg)](https://github.com/yashasviyadav30/Grid-Pathfinder/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)
![Tests](https://img.shields.io/badge/tests-256-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Six pathfinding algorithms on a 2D grid, side by side, so you can watch them
disagree. No dependencies beyond the standard library.

```
        A*                        BFS
S * * * * *              S . . . . .
. . # # . *              * . # # . .
. . # . . *              * . # . . .
. . # . . *              * . # . . .
. # # . . *              * # # . . .
. . . . . E              * * * * * E
   length: 11               length: 11
```

Same grid, same length, different route. A* is pulled toward the goal by its
heuristic; BFS spreads evenly and happens to find the other side first.

## What it does

Shows how different pathfinding algorithms work on a 2D grid. You pick an algorithm, it finds a path from start to end while avoiding walls, then shows you the result.

## Why I made this

Wanted to understand how pathfinding actually works instead of just reading about it. Games use these algorithms all the time - like how enemies chase you or NPCs walk around obstacles. So I implemented the most common ones and made a simple visualizer.

## Algorithms

**BFS (Breadth-First Search)**
- Explores all neighbors before going deeper
- Always finds shortest path
- Uses a queue

**DFS (Depth-First Search)**
- Goes as deep as possible first
- Doesn't guarantee shortest path
- Uses a stack
- Fast but path can be weird

**Dijkstra**
- Classic shortest path algorithm
- Works with weighted graphs too
- Uses priority queue
- Bit slower than BFS on uniform grids

**A\* (A-Star)**
- Smart version of Dijkstra
- Uses heuristic (Manhattan distance) to guide search
- Fastest for most cases
- Popular in games and robotics

**Greedy Best-First**
- Only looks at heuristic, ignores actual distance
- Very fast but doesn't guarantee shortest path
- Good when you need quick results

**Bidirectional BFS**
- Searches from both start and end simultaneously
- Faster than regular BFS
- Still finds shortest path

## How to run

Python 3.9 or newer. There is nothing to install — the code uses only
`collections` and `heapq` from the standard library.

```bash
git clone https://github.com/yashasviyadav30/Grid-Pathfinder.git
cd Grid-Pathfinder
python project.py
```

Pick an algorithm by number, or press `7` to run all six over the same grid and
compare them.

Reading the output: `S` start, `E` end, `#` wall, `*` the path, `.` open ground.

## Tests

256 tests. `test_project.py` covers specific hand-built grids;
`test_path_validity.py` adds property tests over 25 randomised layouts.

```bash
pip install -r requirements-dev.txt
pytest
```

The property tests assert what has to be true of *any* result:

- a path starts at the start and ends at the end
- every step moves exactly one cell
- no step lands on a wall or leaves the grid
- no cell is visited twice
- if one algorithm finds a route, all six do
- BFS, Dijkstra and A\* always agree on the shortest length
- nothing ever returns a path shorter than BFS

CI runs them on Python 3.9 through 3.12.

## Files

```
project.py             the six algorithms, grid builder, and CLI
test_project.py        per-algorithm tests on fixed grids
test_path_validity.py  property tests on randomised grids
```

## Licence

MIT. See [LICENSE](LICENSE).

 
