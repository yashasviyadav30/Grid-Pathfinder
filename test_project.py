from project import bfs, dfs, dijkstra, astar, greedy, bidirectional_bfs, make_grid

# helper grids
def simple():
    return make_grid(3, 3, [])

def wall_wala():
    return make_grid(5, 5, [(0,2),(1,2),(2,2),(3,2)])

def blocked():
    return make_grid(3, 3, [(1,1),(1,2),(2,1)])


# BFS tests
def test_bfs_basic():
    g = simple()
    p = bfs(g, (0,0), (2,2))
    assert p[0] == (0,0)
    assert p[-1] == (2,2)
    assert len(p) > 0

def test_bfs_shortest():
    g = simple()
    p = bfs(g, (0,0), (2,2))
    assert len(p) == 5  # min steps in 3x3

def test_bfs_blocked():
    g = blocked()
    p = bfs(g, (0,0), (2,2))
    assert p == []

def test_bfs_wall():
    g = wall_wala()
    p = bfs(g, (0,0), (0,4))
    assert len(p) > 0
    assert p[0] == (0,0)
    assert p[-1] == (0,4)

def test_bfs_same():
    g = simple()
    p = bfs(g, (1,1), (1,1))
    assert p == [(1,1)]


# DFS tests
def test_dfs_basic():
    g = simple()
    p = dfs(g, (0,0), (2,2))
    assert p[0] == (0,0)
    assert p[-1] == (2,2)

def test_dfs_blocked():
    g = blocked()
    p = dfs(g, (0,0), (2,2))
    assert p == []

def test_dfs_valid():
    g = simple()
    p = dfs(g, (0,0), (2,2))
    for i in range(len(p)-1):
        r1,c1 = p[i]
        r2,c2 = p[i+1]
        assert abs(r1-r2) + abs(c1-c2) == 1  # adjacent cells


# Dijkstra tests
def test_dijkstra_basic():
    g = simple()
    p = dijkstra(g, (0,0), (2,2))
    assert p[0] == (0,0)
    assert p[-1] == (2,2)

def test_dijkstra_shortest():
    g = simple()
    p = dijkstra(g, (0,0), (2,2))
    assert len(p) == 5

def test_dijkstra_blocked():
    g = blocked()
    p = dijkstra(g, (0,0), (2,2))
    assert p == []


# A* tests
def test_astar_basic():
    g = simple()
    p = astar(g, (0,0), (2,2))
    assert p[0] == (0,0)
    assert p[-1] == (2,2)

def test_astar_shortest():
    g = simple()
    p = astar(g, (0,0), (2,2))
    assert len(p) == 5  # same as BFS on uniform grid

def test_astar_blocked():
    g = blocked()
    p = astar(g, (0,0), (2,2))
    assert p == []

def test_astar_wall():
    g = wall_wala()
    p = astar(g, (0,0), (0,4))
    assert len(p) > 0
    assert p[-1] == (0,4)


# Greedy tests
def test_greedy_basic():
    g = simple()
    p = greedy(g, (0,0), (2,2))
    assert p[0] == (0,0)
    assert p[-1] == (2,2)

def test_greedy_blocked():
    g = blocked()
    p = greedy(g, (0,0), (2,2))
    assert p == []

def test_greedy_finds_path():
    # greedy might not give shortest but should find a path
    g = wall_wala()
    p = greedy(g, (0,0), (0,4))
    assert len(p) > 0


# Bidirectional BFS tests
def test_bibfs_basic():
    g = simple()
    p = bidirectional_bfs(g, (0,0), (2,2))
    assert p[0] == (0,0)
    assert p[-1] == (2,2)

def test_bibfs_shortest():
    g = simple()
    p = bidirectional_bfs(g, (0,0), (2,2))
    assert len(p) == 5

def test_bibfs_blocked():
    g = blocked()
    p = bidirectional_bfs(g, (0,0), (2,2))
    assert p == []

def test_bibfs_same():
    g = simple()
    p = bidirectional_bfs(g, (1,1), (1,1))
    assert p == [(1,1)]


# edge cases
def test_single_cell():
    g = make_grid(1, 1, [])
    p = bfs(g, (0,0), (0,0))
    assert p == [(0,0)]

def test_straight():
    g = make_grid(1, 5, [])
    p = bfs(g, (0,0), (0,4))
    assert len(p) == 5

def test_all_walls():
    walls = [(i,j) for i in range(3) for j in range(3) if (i,j) != (0,0)]
    g = make_grid(3, 3, walls)
    p = bfs(g, (0,0), (2,2))
    assert p == []


# compare algos
def test_bfs_dijkstra_same():
    g = simple()
    p1 = bfs(g, (0,0), (2,2))
    p2 = dijkstra(g, (0,0), (2,2))
    assert len(p1) == len(p2)

def test_optimal_algos_same_length():
    # BFS, Dijkstra, A*, Bi-BFS should give same length
    g = simple()
    st, en = (0,0), (2,2)

    p1 = bfs(g, st, en)
    p2 = dijkstra(g, st, en)
    p3 = astar(g, st, en)
    p4 = bidirectional_bfs(g, st, en)

    assert len(p1) == len(p2) == len(p3) == len(p4)

def test_all_reach():
    g = simple()
    st, en = (0,0), (2,2)

    p1 = bfs(g, st, en)
    p2 = dfs(g, st, en)
    p3 = dijkstra(g, st, en)
    p4 = astar(g, st, en)
    p5 = greedy(g, st, en)
    p6 = bidirectional_bfs(g, st, en)

    assert p1[-1] == en
    assert p2[-1] == en
    assert p3[-1] == en
    assert p4[-1] == en
    assert p5[-1] == en
    assert p6[-1] == en

def test_all_handle_walls():
    # all algos should handle walls properly
    g = wall_wala()
    st, en = (0,0), (0,4)

    algos = [bfs, dfs, dijkstra, astar, greedy, bidirectional_bfs]

    for algo in algos:
        p = algo(g, st, en)
        assert len(p) > 0  # path exists
        assert p[0] == st
        assert p[-1] == en
