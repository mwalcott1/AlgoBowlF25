import random
import time
import copy

random.seed(time.time())
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
# initialize gridCopy as zeroes
gridCopy = [[0 for i in range(c)] for j in range(r)]
for i in range(r):
    for j in range(c):
        # convert input to int (not that this really matters but int comparison is faster I guess)
        gridCopy[i][j] = int(fileContents[i+1][j])'''

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

# keep track of our best score and each of its moves
potentialOutput = [0, 0]

# iterate until we can't find more moves
numRandomIters = 50

for z in range(numRandomIters):
    gridCopy = copy.deepcopy(grid)
    moves = []
    score = 0
    while True:
        # find a valid click to make
        # BOZO METHOD!!!

        # iterate random (i, j) selections until we find a valid move
        checked = []
        tries = 0
        while True:
            tries += 1
            i = random.randint(0, r-1)
            j = random.randint(0, c-1)
            if gridCopy[i][j] != -1 and (i, j) not in checked:
                checked.append((i, j))
                currentBlock = [(i, j)]
                blocksToCheck = [(i, j)]
                while blocksToCheck != []:
                    currentCheck = blocksToCheck[0]
                    # if the block one over exists, and isn't already in our list, and matches color, then add to group
                    # and also list to iter over
                    if currentCheck[0] != 0 and (currentCheck[0]-1, currentCheck[1]) not in currentBlock and gridCopy[currentCheck[0]-1][currentCheck[1]] == gridCopy[currentCheck[0]][currentCheck[1]]:
                        currentBlock.append((currentCheck[0]-1, currentCheck[1]))
                        blocksToCheck.append((currentCheck[0]-1, currentCheck[1]))
                    if currentCheck[0] != r-1 and (currentCheck[0]+1, currentCheck[1]) not in currentBlock and gridCopy[currentCheck[0]+1][currentCheck[1]] == gridCopy[currentCheck[0]][currentCheck[1]]:
                        currentBlock.append((currentCheck[0]+1, currentCheck[1]))
                        blocksToCheck.append((currentCheck[0]+1, currentCheck[1]))
                    if currentCheck[1] != 0 and (currentCheck[0], currentCheck[1]-1) not in currentBlock and gridCopy[currentCheck[0]][currentCheck[1]-1] == gridCopy[currentCheck[0]][currentCheck[1]]:
                        currentBlock.append((currentCheck[0], currentCheck[1]-1))
                        blocksToCheck.append((currentCheck[0], currentCheck[1]-1))
                    if currentCheck[1] != c-1 and (currentCheck[0], currentCheck[1]+1) not in currentBlock and gridCopy[currentCheck[0]][currentCheck[1]+1] == gridCopy[currentCheck[0]][currentCheck[1]]:
                        currentBlock.append((currentCheck[0], currentCheck[1]+1))
                        blocksToCheck.append((currentCheck[0], currentCheck[1]+1))
                    # remove thing we're currently checking from stack
                    blocksToCheck.pop(0)
                if len(currentBlock) > 1 or tries > r*c:
                    break

        # if we didn't find a valid click, we are done and can break out of the while loop
        if len(currentBlock) < 2:
            break
        # what color did we remove (important to store now as we change the gridCopy soon)
        colRemoved = gridCopy[currentBlock[0][0]][currentBlock[0][1]]

        # each move is defined by 1. the color removed 2. the num of blocks removed 3/4 the row/col of any block removed
        # locations are indexed frmo bottom left so we convert as well
        moves.append([colRemoved, len(currentBlock), r - currentBlock[0][0], currentBlock[0][1]+1])

        # GRAVITY (filter down, then left if empty column)
        for (i, j) in currentBlock:
            gridCopy[i][j] = -1
        # save non-removed things in each row and append -1s on top
        for j in range(c):
            newCol = [gridCopy[i][j] for i in range(r) if gridCopy[i][j] != -1]
            for i in range(r):
                if i < r - len(newCol):
                    gridCopy[i][j] = -1
                else:
                    gridCopy[i][j] = newCol[i - (r - len(newCol))]

        # now if we have an empty column, move everything to the left
        k = 0
        # prevent infinite loop
        LoopIters = 0
        while k < c and LoopIters < c:
            if gridCopy[r-1][k] == -1:
                for j in range(k, c-1):
                    for i in range(r):
                        gridCopy[i][j] = gridCopy[i][j+1]
                # make sure the last column is all -1s (all other removals should ensure that col is -1s automatically)
                for i in range(r):
                    gridCopy[i][-1] = -1
                LoopIters += 1
            else:
                k += 1
        # END GRAVITY SECTION

        # repeat this loop until we can't find a valid click

    # tally score:
    score = 0
    for move in moves:
        score += (move[1] - 1)**2

    if score > potentialOutput[0]:
        potentialOutput = [score, moves]

# output!!
# format: score, then total num of moves, then details of each move
print(potentialOutput[0])
print(len(potentialOutput[1]))
for move in potentialOutput[1]:
    print(f'{move[0]} {move[1]} {move[2]} {move[3]}')
