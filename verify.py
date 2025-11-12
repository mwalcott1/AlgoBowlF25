"""
Same Game Verifier
Validates solutions for the AlgoBOWL problem.
"""

import sys
from copy import deepcopy

def read_input(input_file):
    """Read and parse the input file."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Parse dimensions
    r, c = map(int, lines[0].split())
    
    # Parse grid (store with row 0 at top, matching solver.py)
    grid = []
    for i in range(r):
        row = [int(ch) for ch in lines[i + 1].strip()]
        grid.append(row)
    
    return r, c, grid

def read_output(output_file):
    """Read and parse the output file."""
    with open(output_file, 'r') as f:
        lines = f.readlines()
    
    claimed_score = int(lines[0].strip())
    num_moves = int(lines[1].strip())
    
    moves = []
    for i in range(num_moves):
        parts = lines[i + 2].split()
        color = int(parts[0])
        count = int(parts[1])
        row = int(parts[2])  # 1-indexed from bottom
        col = int(parts[3])  # 1-indexed from left
        moves.append((color, count, row, col))
    
    return claimed_score, moves

def find_connected_component(grid, r, c, start_row, start_col, color):
    """
    Find all squares connected to the starting position with the same color
    Using BFS to find the connected component
    Returns a list of (row, col) tuples
    """
    if grid[start_row][start_col] != color or grid[start_row][start_col] == -1:
        return []
    
    visited = set()
    to_check = [(start_row, start_col)]
    component = []
    
    while to_check:
        curr_row, curr_col = to_check.pop(0)
        
        if (curr_row, curr_col) in visited:
            continue
        
        visited.add((curr_row, curr_col))
        component.append((curr_row, curr_col))
        
        # Check all 4 adjacent cells
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = curr_row + dr, curr_col + dc
            if (0 <= new_row < r and 0 <= new_col < c and 
                (new_row, new_col) not in visited and
                grid[new_row][new_col] == color):
                to_check.append((new_row, new_col))
    
    return component

def apply_gravity(grid, r, c, removed_blocks):
    """
    Apply gravity after removing blocks
    1. Drop blocks down within each column
    2. Shift columns left if any become empty
    """
    # Drop blocks down
    for i in range(r):
        for j in range(c):
            if (i, j) in removed_blocks:
                # Move everything above down
                for k in range(i):
                    grid[i - k][j] = grid[i - k - 1][j]
                grid[0][j] = -1
    
    # Shift columns left if empty
    k = 0
    loop_iters = 0
    while k < c and loop_iters < c:
        if grid[r - 1][k] == -1:
            # Column k is empty, shift everything left
            for j in range(k, c - 1):
                for i in range(r):
                    grid[i][j] = grid[i][j + 1]
            # Clear the rightmost column
            for i in range(r):
                grid[i][c - 1] = -1
            loop_iters += 1
        else:
            k += 1

def verify_solution(input_file, output_file, verbose=True):
    """
    Verify a solution file against an input file.
    Returns (is_valid, actual_score, error_message)
    """
    try:
        # Read input and output
        r, c, initial_grid = read_input(input_file)
        claimed_score, moves = read_output(output_file)
        
        # Make a working copy of the grid
        grid = deepcopy(initial_grid)
        
        actual_score = 0
        
        if verbose:
            print(f"Input: {r}x{c} grid")
            print(f"Claimed score: {claimed_score}")
            print(f"Number of moves: {len(moves)}")
            print()
        
        # Simulate each move
        for move_num, (color, count, row_1indexed, col_1indexed) in enumerate(moves, 1):
            if verbose:
                print(f"Move {move_num}: Remove {count} squares of color {color} at ({row_1indexed}, {col_1indexed})")
            
            # Convert 1-indexed coordinates (from bottom-left) to 0-indexed (from top-left)
            # Bottom row is 1, top row is r
            # So row_1indexed=1 corresponds to grid[r-1], row_1indexed=r corresponds to grid[0]
            row_0indexed = r - row_1indexed
            col_0indexed = col_1indexed - 1
            
            # Validate coordinates
            if not (0 <= row_0indexed < r and 0 <= col_0indexed < c):
                return False, 0, f"Move {move_num}: Invalid coordinates ({row_1indexed}, {col_1indexed})"
            
            # Check if the specified square exists and has the correct color
            if grid[row_0indexed][col_0indexed] == -1:
                return False, 0, f"Move {move_num}: Square at ({row_1indexed}, {col_1indexed}) is empty"
            
            if grid[row_0indexed][col_0indexed] != color:
                return False, 0, f"Move {move_num}: Square at ({row_1indexed}, {col_1indexed}) has color {grid[row_0indexed][col_0indexed]}, not {color}"
            
            # Find the connected component
            component = find_connected_component(grid, r, c, row_0indexed, col_0indexed, color)
            
            # Verify the count
            if len(component) != count:
                return False, 0, f"Move {move_num}: Claimed {count} squares but found {len(component)} connected squares"
            
            # Verify we're removing at least 2 squares
            if count < 2:
                return False, 0, f"Move {move_num}: Cannot remove fewer than 2 squares (tried to remove {count})"
            
            # Calculate score for this move
            move_score = (count - 1) ** 2
            actual_score += move_score
            
            if verbose:
                print(f"  Found {len(component)} connected squares")
                print(f"  Score for this move: ({count} - 1)^2 = {move_score}")
            
            # Apply the move (remove blocks and apply gravity)
            apply_gravity(grid, r, c, component)
            
            if verbose:
                print()
        
        # Check if the total score matches
        if actual_score != claimed_score:
            return False, actual_score, f"Score mismatch: claimed {claimed_score} but actual is {actual_score}"
        
        if verbose:
            print(f"✓ Solution is VALID")
            print(f"✓ Total score: {actual_score}")
        
        return True, actual_score, "Valid solution"
    
    except Exception as e:
        return False, 0, f"Error during verification: {str(e)}"

def main():
    if len(sys.argv) != 3:
        print("Usage: python verifier.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    is_valid, score, message = verify_solution(input_file, output_file, verbose=True)
    
    if is_valid:
        print(f"\n✓ VALID SOLUTION with score {score}")
        sys.exit(0)
    else:
        print(f"\n✗ INVALID SOLUTION: {message}")
        sys.exit(1)

if __name__ == "__main__":
    main()