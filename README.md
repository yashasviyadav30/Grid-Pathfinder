# Path Finder

Grid pathfinding algorithms visualizer.

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

Install dependencies:
```bash
pip install -r requirements.txt

