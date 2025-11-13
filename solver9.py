# Same Game solver — Fast greedy by largest component

from collections import deque

# ----- read input (top rows first) -----
sizes = input().split()
r, c = int(sizes[0]), int(sizes[1])
grid = [[0]*c for _ in range(r)]
for i in range(r):
    row = input().strip()
    for j in range(c):
        grid[i][j] = int(row[j])

def neigh(i, j):
    if i > 0:     yield i-1, j
    if i+1 < r:   yield i+1, j
    if j > 0:     yield i, j-1
    if j+1 < c:   yield i, j+1

def bfs_count(i0, j0, seen):
    """Count size of the component at (i0,j0) (without building the whole list)."""
    color = grid[i0][j0]
    q = deque([(i0, j0)])
    seen[i0][j0] = True
    size = 0
    while q:
        i, j = q.popleft()
        size += 1
        for x, y in neigh(i, j):
            if not seen[x][y] and grid[x][y] == color:
                seen[x][y] = True
                q.append((x, y))
    return size

def bfs_collect(i0, j0):
    """Collect all cells in the component at (i0,j0)."""
    color = grid[i0][j0]
    q = deque([(i0, j0)])
    comp = [(i0, j0)]
    mark = [[False]*c for _ in range(r)]
    mark[i0][j0] = True
    while q:
        i, j = q.popleft()
        for x, y in neigh(i, j):
            if not mark[x][y] and grid[x][y] == color:
                mark[x][y] = True
                comp.append((x, y))
                q.append((x, y))
    return comp

def apply_gravity_and_shift():
    # collapse each column down using a write pointer
    for j in range(c):
        write = r - 1
        for i in range(r-1, -1, -1):
            if grid[i][j] != -1:
                grid[write][j] = grid[i][j]
                write -= 1
        for i in range(write, -1, -1):
            grid[i][j] = -1

    # shift non-empty columns left
    write_col = 0
    for j in range(c):
        # check if column j is non-empty
        non_empty = False
        for i in range(r):
            if grid[i][j] != -1:
                non_empty = True
                break
        if non_empty:
            if j != write_col:
                for i in range(r):
                    grid[i][write_col] = grid[i][j]
            write_col += 1
    # blank the rest
    for j in range(write_col, c):
        for i in range(r):
            grid[i][j] = -1

moves = []

while True:
    # ---- pass 1: find largest component seed (no big lists) ----
    seen = [[False]*c for _ in range(r)]
    best_size = 0
    best_seed = None

    for i in range(r):
        for j in range(c):
            if grid[i][j] == -1 or seen[i][j]:
                continue
            size = bfs_count(i, j, seen)
            if size >= 2 and size > best_size:
                best_size = size
                best_seed = (i, j)

    # no move left
    if best_size < 2:
        break

    # ---- pass 2: collect & remove that single best component ----
    comp = bfs_collect(*best_seed)
    color = grid[best_seed[0]][best_seed[1]]

    # record move (any cell in the comp is acceptable for reporting)
    i0, j0 = comp[0]
    moves.append([color, len(comp), r - i0, j0 + 1])

    # remove
    for i, j in comp:
        grid[i][j] = -1

    # gravity + shift
    apply_gravity_and_shift()

# score
score = sum((n - 1)**2 for _, n, _, _ in moves)

# output
print(score)
print(len(moves))
for m in moves:
    print(m[0], m[1], m[2], m[3])
