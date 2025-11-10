# Same Game solver
# Goal is not to clear the board but to maximize score

# open input file
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
        grid[i][j] = int(fileContents[i+1][j])

while True:
    # store the blocks in the chunk we're clicking on (for scoring/gravity purposes)
    currentBlock = []

    # find a valid click to make
    # right now, just finds the first valid click available. Could be made much better to maximize score.
    for i in range(r):
        for j in range(c):
            # if adjacent blocks exists and matches color, we'll click. Also we'll add both blocks to the current chunk.
            if i != 0 and grid[i-1][j] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i-1, j))
                break
            if i != r-1 and grid[i+1][j] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i+1, j))
                break
            if j != 0 and grid[i][j-1] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i, j-1))
                break
            if j != c-1 and grid[i][j+1] == grid[i][j]:
                currentBlock.append((i, j))
                currentBlock.append((i, j+1))
                break
        if currentBlock != []:
            break

    # find rest of blocks in chunk
    blocksToCheck = [currentBlock[0], currentBlock[1]]
    while blocksToCheck != []:
        currentCheck = blocksToCheck[-1]
        # if the block one over exists, and isn't already in our list, and matches color, then add to group
        # and also list to iter over
        if currentCheck[0] != 0 and (currentCheck[0]-1, currentCheck[1]) not in currentBlock and grid[currentCheck[0]-1][currentCheck[1]] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck-1, j))
            blocksToCheck.append((currentCheck-1, j))
        if currentCheck[0] != r-1 and (currentCheck[0]+1, currentCheck[1]) not in currentBlock and grid[currentCheck[0]+1][currentCheck[1]] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck-1, j))
            blocksToCheck.append((currentCheck-1, j))
        if currentCheck[1] != 0 and (currentCheck[0], currentCheck[1]-1) not in currentBlock and grid[currentCheck[0]][currentCheck[1]-1] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck-1, j))
            blocksToCheck.append((currentCheck-1, j))
        if currentCheck[0] != c-1 and (currentCheck[0]+1, currentCheck[1]) not in currentBlock and grid[currentCheck[0]][currentCheck[1]+1] == grid[currentCheck[0]][currentCheck[1]]:
            currentBlock.append((currentCheck-1, j))
            blocksToCheck.append((currentCheck-1, j))
        # remove thing we're currently checking from queue
        blocksToCheck.pop()

    # STILL TO IMPLEMENT:
    # GRAVITY (filter down, then left if empty column)
    # RE-CHOICE (we ideally want to click on more than one place)
    # TALLYING SCORE/FORMATTING OUTPUT

    # THEN, work on improving selection algorithm.

    break
# testing output
'''
print(f'First click done, clicked on: ({currentBlock[0][0]}, {currentBlock[0][1]}). List of blocks in chunk:')
print(currentBlock)
'''
