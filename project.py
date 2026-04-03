# pathfinding algos - bfs, dfs, dijkstra, a*, greedy, bidirectional bfs

from collections import deque
import heapq

# building grid - 1 means wall, 0 means khali
def make_grid(n, m, walls):
    g = [[0]*m for _ in range(n)]
    for x, y in walls:
        g[x][y] = 1
    return g

# 4 directions - up down left right
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def bfs(g, st, en):
    q = deque([st])
    vis = set([st])
    parent = {st: None}

    while q:
        curr = q.popleft()

        if curr == en:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        r, c = curr
        for i in range(4):
            nr, nc = r + dx[i], c + dy[i]

            if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                nxt = (nr, nc)
                if nxt not in vis:
                    vis.add(nxt)
                    parent[nxt] = curr
                    q.append(nxt)

    return []

def dfs(g, st, en):
    stk = [st]
    vis = set([st])
    parent = {st: None}

    while stk:
        curr = stk.pop()

        if curr == en:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        r, c = curr
        for i in range(4):
            nr, nc = r + dx[i], c + dy[i]

            if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                nxt = (nr, nc)
                if nxt not in vis:
                    vis.add(nxt)
                    parent[nxt] = curr
                    stk.append(nxt)

    return []

def dijkstra(g, st, en):
    pq = [(0, st)]
    dist = {st: 0}
    parent = {st: None}

    while pq:
        d, curr = heapq.heappop(pq)

        if curr == en:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        if d > dist.get(curr, float('inf')):
            continue

        r, c = curr
        for i in range(4):
            nr, nc = r + dx[i], c + dy[i]

            if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                nxt = (nr, nc)
                new_dist = d + 1

                if new_dist < dist.get(nxt, float('inf')):
                    dist[nxt] = new_dist
                    parent[nxt] = curr
                    heapq.heappush(pq, (new_dist, nxt))

    return []

def astar(g, st, en):
    # heuristic - manhattan distance
    def h(node):
        return abs(node[0] - en[0]) + abs(node[1] - en[1])

    pq = [(h(st), 0, st)]  # (f_cost, g_cost, node)
    parent = {st: None}
    cost = {st: 0}

    while pq:
        _, g_cost, curr = heapq.heappop(pq)

        if curr == en:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        if g_cost > cost.get(curr, float('inf')):
            continue

        r, c = curr
        for i in range(4):
            nr, nc = r + dx[i], c + dy[i]

            if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                nxt = (nr, nc)
                new_cost = cost[curr] + 1

                if new_cost < cost.get(nxt, float('inf')):
                    cost[nxt] = new_cost
                    f_cost = new_cost + h(nxt)
                    parent[nxt] = curr
                    heapq.heappush(pq, (f_cost, new_cost, nxt))

    return []

def greedy(g, st, en):
    # only heuristic use karta hai
    def h(node):
        return abs(node[0] - en[0]) + abs(node[1] - en[1])

    pq = [(h(st), st)]
    parent = {st: None}
    vis = set()

    while pq:
        _, curr = heapq.heappop(pq)

        if curr in vis:
            continue
        vis.add(curr)

        if curr == en:
            path = []
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        r, c = curr
        for i in range(4):
            nr, nc = r + dx[i], c + dy[i]

            if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                nxt = (nr, nc)
                if nxt not in vis:
                    parent[nxt] = curr
                    heapq.heappush(pq, (h(nxt), nxt))

    return []

def bidirectional_bfs(g, st, en):
    if st == en:
        return [st]

    # dono sides se search
    q1, q2 = deque([st]), deque([en])
    vis1, vis2 = {st: None}, {en: None}

    while q1 or q2:
        # forward search
        if q1:
            curr = q1.popleft()
            r, c = curr

            for i in range(4):
                nr, nc = r + dx[i], c + dy[i]
                if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                    nxt = (nr, nc)

                    if nxt in vis2:  # paths meet
                        p1, p2 = [], []
                        temp = curr
                        while temp:
                            p1.append(temp)
                            temp = vis1[temp]
                        temp = nxt
                        while temp:
                            p2.append(temp)
                            temp = vis2[temp]
                        return p1[::-1] + p2

                    if nxt not in vis1:
                        vis1[nxt] = curr
                        q1.append(nxt)

        # backward search
        if q2:
            curr = q2.popleft()
            r, c = curr

            for i in range(4):
                nr, nc = r + dx[i], c + dy[i]
                if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] == 0:
                    nxt = (nr, nc)

                    if nxt in vis1:  # paths meet
                        p1, p2 = [], []
                        temp = nxt
                        while temp:
                            p1.append(temp)
                            temp = vis1[temp]
                        temp = curr
                        while temp:
                            p2.append(temp)
                            temp = vis2[temp]
                        return p1[::-1] + p2

                    if nxt not in vis2:
                        vis2[nxt] = curr
                        q2.append(nxt)

    return []

# printing the grid
def show(g, path, st, en):
    p_set = set(path)
    for i in range(len(g)):
        for j in range(len(g[0])):
            if (i,j) == st:
                print('S', end=' ')
            elif (i,j) == en:
                print('E', end=' ')
            elif (i,j) in p_set:
                print('*', end=' ')
            elif g[i][j] == 1:
                print('#', end=' ')
            else:
                print('.', end=' ')
        print()
    print(f"length: {len(path)}\n" if path else "no path\n")


def main():
    # test case
    walls = [(1,2), (2,2), (3,2), (1,3), (4,1), (4,2)]
    grid = make_grid(6, 6, walls)
    start = (0, 0)
    end = (5, 5)

    print("\n1. BFS")
    print("2. DFS")
    print("3. Dijkstra")
    print("4. A* (fastest)")
    print("5. Greedy Best-First")
    print("6. Bidirectional BFS")
    print("7. Compare all\n")

    ch = input("choice: ")

    if ch == '1':
        print("\n--- BFS ---")
        p = bfs(grid, start, end)
        show(grid, p, start, end)

    elif ch == '2':
        print("\n--- DFS ---")
        p = dfs(grid, start, end)
        show(grid, p, start, end)

    elif ch == '3':
        print("\n--- Dijkstra ---")
        p = dijkstra(grid, start, end)
        show(grid, p, start, end)

    elif ch == '4':
        print("\n--- A* ---")
        p = astar(grid, start, end)
        show(grid, p, start, end)

    elif ch == '5':
        print("\n--- Greedy Best-First ---")
        p = greedy(grid, start, end)
        show(grid, p, start, end)

    elif ch == '6':
        print("\n--- Bidirectional BFS ---")
        p = bidirectional_bfs(grid, start, end)
        show(grid, p, start, end)

    elif ch == '7':
        algos = [
            (bfs, "BFS"),
            (dfs, "DFS"),
            (dijkstra, "Dijkstra"),
            (astar, "A*"),
            (greedy, "Greedy"),
            (bidirectional_bfs, "Bi-BFS")
        ]

        for algo, name in algos:
            print(f"\n--- {name} ---")
            show(grid, algo(grid, start, end), start, end)
            input("Press Enter...")

    else:
        print("wrong choice")


if __name__ == "__main__":
    main()
 
