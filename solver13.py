#!/usr/bin/env python3
"""
Same Game Solver
"""

import sys
from collections import deque

class SameGameSolver:
    def __init__(self, rows, cols, grid):
        self.rows = rows
        self.cols = cols
        self.grid = [row[:] for row in grid]
        self.moves = []
        self.score = 0

    def find_connected_component(self, row, col):
        """Fast BFS to find connected component """
        color = self.grid[row][col]
        if color == -1:
            return []
        
        visited = set()
        queue = deque([(row, col)])
        component = []
        
        while queue:
            r, c = queue.popleft()
            
            if (r, c) in visited:
                continue
            
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                continue
                
            if self.grid[r][c] != color:
                continue
            
            visited.add((r, c))
            component.append((r, c))
            
            # Add neighbors
            queue.append((r-1, c))
            queue.append((r+1, c))
            queue.append((r, c-1))
            queue.append((r, c+1))
        
        return component
    
    def apply_gravity(self, component):
        """Optimized gravity application """
        # Mark removed squares
        for r, c in component:
            self.grid[r][c] = -1
        
        # Drop blocks down in each column
        for col in range(self.cols):
            # Write position starts at bottom
            write_pos = self.rows - 1
            
            # Read from bottom to top
            for read_pos in range(self.rows - 1, -1, -1):
                if self.grid[read_pos][col] != -1:
                    if write_pos != read_pos:
                        self.grid[write_pos][col] = self.grid[read_pos][col]
                        self.grid[read_pos][col] = -1
                    write_pos -= 1
        
        # Shift columns left
        write_col = 0
        for read_col in range(self.cols):
            if self.grid[self.rows - 1][read_col] != -1:
                if write_col != read_col:
                    for row in range(self.rows):
                        self.grid[row][write_col] = self.grid[row][read_col]
                        self.grid[row][read_col] = -1
                write_col += 1
    
    def find_all_moves(self):
        """Find all valid moves """
        moves = []
        checked = [[False] * self.cols for _ in range(self.rows)]
        
        for i in range(self.rows):
            for j in range(self.cols):
                if not checked[i][j] and self.grid[i][j] != -1:
                    component = self.find_connected_component(i, j)
                    
                    if len(component) >= 2:
                        moves.append({
                            'component': component,
                            'color': self.grid[i][j],
                            'size': len(component),
                            'score': (len(component) - 1) ** 2,
                            'pos': (i, j)
                        })
                    
                    # Mark all squares in component as checked
                    for r, c in component:
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            checked[r][c] = True
        
        return moves
    
    def solve_greedy_largest(self):
        """Fast greedy: always pick largest group """
        iterations = 0
        max_iterations = 100000  # Safety limit
        
        while iterations < max_iterations:
            iterations += 1
            moves = self.find_all_moves()
            
            if not moves:
                break
            
            # Pick largest group
            best_move = max(moves, key=lambda m: (m['size'], m['score']))
            
            # Record move
            r, c = best_move['pos']
            output_row = self.rows - r
            output_col = c + 1
            
            self.moves.append([
                best_move['color'],
                best_move['size'],
                output_row,
                output_col
            ])
            self.score += best_move['score']
            
            # Apply move
            self.apply_gravity(best_move['component'])
        
        return self.score
    
    def solve_greedy_score_then_size(self):
        """Greedy: prefer high score, break ties with size """
        iterations = 0
        max_iterations = 100000
        
        while iterations < max_iterations:
            iterations += 1
            moves = self.find_all_moves()
            
            if not moves:
                break
            
            # Pick best score, then largest size
            best_move = max(moves, key=lambda m: (m['score'], m['size']))
            
            r, c = best_move['pos']
            output_row = self.rows - r
            output_col = c + 1
            
            self.moves.append([
                best_move['color'],
                best_move['size'],
                output_row,
                output_col
            ])
            self.score += best_move['score']
            
            self.apply_gravity(best_move['component'])
        
        return self.score
    
    def solve_fast(self):
        """Really fast solver for large inputs """
        iterations = 0
        max_iterations = 50000
        
        while iterations < max_iterations:
            iterations += 1
            
            # Find first large group (size >= 5) or best available
            best_move = None
            best_score = 0
            checked = [[False] * self.cols for _ in range(self.rows)]
            
            for i in range(self.rows):
                for j in range(self.cols):
                    if not checked[i][j] and self.grid[i][j] != -1:
                        component = self.find_connected_component(i, j)
                        
                        for r, c in component:
                            if 0 <= r < self.rows and 0 <= c < self.cols:
                                checked[r][c] = True
                        
                        if len(component) >= 2:
                            score = (len(component) - 1) ** 2
                            
                            # Take first group of 5+ immediately
                            if len(component) >= 5:
                                best_move = {
                                    'component': component,
                                    'color': self.grid[i][j],
                                    'size': len(component),
                                    'score': score,
                                    'pos': (i, j)
                                }
                                break
                            
                            if score > best_score:
                                best_score = score
                                best_move = {
                                    'component': component,
                                    'color': self.grid[i][j],
                                    'size': len(component),
                                    'score': score,
                                    'pos': (i, j)
                                }
                
                if best_move and best_move['size'] >= 5:
                    break
            
            if not best_move:
                break
            
            r, c = best_move['pos']
            output_row = self.rows - r
            output_col = c + 1
            
            self.moves.append([
                best_move['color'],
                best_move['size'],
                output_row,
                output_col
            ])
            self.score += best_move['score']
            
            self.apply_gravity(best_move['component'])
        
        return self.score
    
    def output_solution(self):
        print(self.score)
        print(len(self.moves))
        for move in self.moves:
            print(f"{move[0]} {move[1]} {move[2]} {move[3]}")


def main():
    # Read input
    try:
        sizes = input().split()
        r = int(sizes[0])
        c = int(sizes[1])
        
        grid = []
        for i in range(r):
            row = input().strip()
            grid.append([int(ch) for ch in row])
        
        # Choose strategy based on grid size
        grid_size = r * c
        
        if grid_size > 5000:
            # Very large - use fastest solver
            solver = SameGameSolver(r, c, grid)
            solver.solve_fast()
        elif grid_size > 1000:
            # Large - use greedy 
            solver = SameGameSolver(r, c, grid)
            solver.solve_greedy_largest()
        else:
            # Small - try multiple strats
            best_solver = None
            best_score = -1
            
            for strategy in [
                lambda s: s.solve_greedy_largest(),
                lambda s: s.solve_greedy_score_then_size(),
            ]:
                s = SameGameSolver(r, c, grid)
                strategy(s)
                if s.score > best_score:
                    best_score = s.score
                    best_solver = s
            
            solver = best_solver
        
        solver.output_solution()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        # Output empty solution rather than crashing out
        print(0)
        print(0)
        sys.exit(1)

if __name__ == "__main__":
    main()