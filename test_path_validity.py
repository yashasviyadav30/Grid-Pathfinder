"""Property tests: whatever an algorithm returns has to be a path you could walk.

test_project.py checks specific grids. These check invariants that must hold on
every grid, using randomised layouts so the cases aren't hand-picked.
"""

import random

import pytest

from project import (
    make_grid, bfs, dfs, dijkstra, astar, greedy, bidirectional_bfs,
)

ALL_ALGORITHMS = [
    (bfs, "bfs"),
    (dfs, "dfs"),
    (dijkstra, "dijkstra"),
    (astar, "astar"),
    (greedy, "greedy"),
    (bidirectional_bfs, "bidirectional_bfs"),
]

# BFS, Dijkstra and A* are all guaranteed to return a shortest path on an
# unweighted grid. Greedy and DFS are not, by design.
OPTIMAL_ALGORITHMS = [(bfs, "bfs"), (dijkstra, "dijkstra"), (astar, "astar")]


def random_grid(seed, rows=8, cols=8, wall_ratio=0.25):
    """A grid with random walls, start at the top left and end at the bottom right."""
    rng = random.Random(seed)
    walls = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if rng.random() < wall_ratio and (r, c) not in {(0, 0), (rows - 1, cols - 1)}
    ]
    return make_grid(rows, cols, walls), (0, 0), (rows - 1, cols - 1)


def assert_walkable(grid, path, start, end, name):
    """A returned path must begin at start, end at end, step one cell at a time,
    and never cross a wall."""
    if not path:
        return

    assert path[0] == start, f"{name}: path starts at {path[0]}, not {start}"
    assert path[-1] == end, f"{name}: path ends at {path[-1]}, not {end}"

    for cell in path:
        r, c = cell
        assert 0 <= r < len(grid) and 0 <= c < len(grid[0]), f"{name}: {cell} is off-grid"
        assert grid[r][c] == 0, f"{name}: path crosses a wall at {cell}"

    for before, after in zip(path, path[1:]):
        step = abs(before[0] - after[0]) + abs(before[1] - after[1])
        assert step == 1, f"{name}: {before} and {after} are not adjacent"

    assert len(set(path)) == len(path), f"{name}: path revisits a cell"


@pytest.mark.parametrize("algorithm,name", ALL_ALGORITHMS)
@pytest.mark.parametrize("seed", range(25))
def test_returned_path_is_walkable(algorithm, name, seed):
    grid, start, end = random_grid(seed)
    assert_walkable(grid, algorithm(grid, start, end), start, end, name)


@pytest.mark.parametrize("seed", range(25))
def test_algorithms_agree_on_reachability(seed):
    """If one algorithm finds a route, all of them must."""
    grid, start, end = random_grid(seed)
    found = {name: bool(algorithm(grid, start, end)) for algorithm, name in ALL_ALGORITHMS}
    assert len(set(found.values())) == 1, f"algorithms disagree on seed {seed}: {found}"


@pytest.mark.parametrize("seed", range(25))
def test_optimal_algorithms_return_the_same_length(seed):
    grid, start, end = random_grid(seed)
    lengths = {
        name: len(algorithm(grid, start, end)) for algorithm, name in OPTIMAL_ALGORITHMS
    }
    assert len(set(lengths.values())) == 1, f"shortest-path lengths differ: {lengths}"


@pytest.mark.parametrize("seed", range(25))
def test_no_algorithm_beats_the_shortest_path(seed):
    """DFS and greedy may be longer, but nothing can be shorter than BFS."""
    grid, start, end = random_grid(seed)
    shortest = len(bfs(grid, start, end))
    if not shortest:
        return
    for algorithm, name in ALL_ALGORITHMS:
        length = len(algorithm(grid, start, end))
        if length:
            assert length >= shortest, f"{name} returned {length}, shorter than BFS {shortest}"


def test_start_equals_end_returns_that_single_cell():
    grid = make_grid(4, 4, [])
    for algorithm, name in ALL_ALGORITHMS:
        path = algorithm(grid, (2, 2), (2, 2))
        assert path == [(2, 2)], f"{name} returned {path}"


def test_fully_walled_end_is_unreachable():
    grid = make_grid(5, 5, [(3, 4), (4, 3)])
    for algorithm, name in ALL_ALGORITHMS:
        assert algorithm(grid, (0, 0), (4, 4)) == [], f"{name} found a way through walls"
