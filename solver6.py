# Same Game solver
# Goal is not to clear the board but to maximize score

# Note: to run this file with my current test inputs (which are just our problem inputs), you can run:
# make test
# in a bash terminal. Note that this will overwrite anything in testOutput.txt in your current directory.

# file input
'''# open input file
fileName = input()
file = open(fileName, "r")
fileContents = file.readlines()
# extract rows and columns
line1 = fileContents[0].split()
r = int(line1[0])
c = int(line1[1])
# initialize grid as zeroes
grid = [[0 for i in range(c)] for j in range(r)]
for i in range(r):
    for j in range(c):
        # convert input to int (not that this really matters but int comparison is faster I guess)
        grid[i][j] = int(fileContents[i+1][j])'''

# text input
sizes = input().split()
r = int(sizes[0])
c = int(sizes[1])
grid = [[0 for i in range(c)] for j in range(r)]
for i in range(r):
    currentRow = input()
    for j in range(c):
        # convert input to int (not that this really matters but int comparison is faster I guess)
        grid[i][j] = int(currentRow[j])

# keep track of our total score and each of our moves
score = 0
moves = []

# iterate until we can't find more moves
while True:

    # store the blocks in the chunk we're clicking on (for scoring/gravity purposes)
    currentBlock = []

    # find a valid click to make
    # right now, just finds the first valid click available. Could be made much better to maximize score.
    for j in range(c-1, -1, -1):
        for i in range(r):
            # if adjacent blocks exists and matches color, we'll click. Also we'll add both blocks to the current chunk.
            # if the 'color' is -1, that's an empty space and we can't click there
            if i != 0 and grid[i][j] != -1 and grid[i-1][j] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i-1, j))
                break
            if i != r-1 and grid[i][j] != -1 and grid[i+1][j] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i+1, j))
                break
            if j != 0 and grid[i][j] != -1 and grid[i][j-1] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i, j-1))
                break
            if j != c-1 and grid[i][j] != -1 and grid[i][j+1] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i, j+1))
                break
        if currentBlock != []:
            break

    # if we didn't find a valid click, we are done and can break out of the while loop
    if len(currentBlock) == 0:
        break

    # what color did we remove (important to store now as we change the grid soon)
    colRemoved = grid[currentBlock[0][0]][currentBlock[0][1]]

    # find rest of blocks in chunk
    blocksToCheck = [currentBlock[0], currentBlock[1]]
    while blocksToCheck != []:
        currentCheck = blocksToCheck[0]
        # if the block one over exists, and isn't already in our list, and matches color, then add to group
        # and also list to iter over
        if currentCheck[0] != 0 and (currentCheck[0]-1, currentCheck[1]) not in currentBlock and grid[currentCheck[0]-1][currentCheck[1]] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck[0]-1, currentCheck[1]))
            blocksToCheck.append((currentCheck[0]-1, currentCheck[1]))
        if currentCheck[0] != r-1 and (currentCheck[0]+1, currentCheck[1]) not in currentBlock and grid[currentCheck[0]+1][currentCheck[1]] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck[0]+1, currentCheck[1]))
            blocksToCheck.append((currentCheck[0]+1, currentCheck[1]))
        if currentCheck[1] != 0 and (currentCheck[0], currentCheck[1]-1) not in currentBlock and grid[currentCheck[0]][currentCheck[1]-1] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck[0], currentCheck[1]-1))
            blocksToCheck.append((currentCheck[0], currentCheck[1]-1))
        if currentCheck[1] != c-1 and (currentCheck[0], currentCheck[1]+1) not in currentBlock and grid[currentCheck[0]][currentCheck[1]+1] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck[0], currentCheck[1]+1))
            blocksToCheck.append((currentCheck[0], currentCheck[1]+1))
        # remove thing we're currently checking from stack
        blocksToCheck.pop(0)

    # each move is defined by 1. the color removed 2. the num of blocks removed 3/4 the row/col of any block removed
    # locations are indexed frmo bottom left so we convert as well
    moves.append([colRemoved, len(currentBlock), r - currentBlock[0][0], currentBlock[0][1]+1])

    # GRAVITY (filter down, then left if empty column)
    for (i, j) in currentBlock:
        grid[i][j] = -1
    # save non-removed things in each row and append -1s on top
    for j in range(c):
        newCol = [grid[i][j] for i in range(r) if grid[i][j] != -1]
        for i in range(r):
            if i < r - len(newCol):
                grid[i][j] = -1
            else:
                grid[i][j] = newCol[i - (r - len(newCol))]

    # now if we have an empty column, move everything to the left
    k = 0
    # prevent infinite loop
    LoopIters = 0
    while k < c and LoopIters < c:
        if grid[r-1][k] == -1:
            for j in range(k, c-1):
                for i in range(r):
                    grid[i][j] = grid[i][j+1]
            # make sure the last column is all -1s (all other removals should ensure that col is -1s automatically)
            for i in range(r):
                grid[i][-1] = -1
            LoopIters += 1
        else:
            k += 1
    # END GRAVITY SECTION

    # repeat this loop until we can't find a valid click

# tally score:
score = 0
for move in moves:
    score += (move[1] - 1)**2

# output!!
# format: score, then total num of moves, then details of each move
print(score)
print(len(moves))
for move in moves:
    print(f'{move[0]} {move[1]} {move[2]} {move[3]}')
