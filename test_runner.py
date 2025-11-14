#!/usr/bin/env python3
"""
Test Runner for Same Game Solver
Runs the solver on multiple input files and optionally verifies outputs.
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

def run_solver_on_file(solver_script, input_file, output_file):
    """
    Run the solver on a single input file and save output.
    Returns (success, score, error_message)
    """
    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
        
        # Run the solver
        result = subprocess.run(
            ['python3', solver_script],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode != 0:
            return False, 0, f"Solver error: {result.stderr}"
        
        # Save output
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        
        # Extract score from first line
        lines = result.stdout.strip().split('\n')
        if lines:
            score = int(lines[0])
            return True, score, None
        else:
            return False, 0, "No output from solver"
    
    except subprocess.TimeoutExpired:
        return False, 0, "Solver timeout (30s)"
    except Exception as e:
        return False, 0, f"Error: {str(e)}"

def verify_solution(verifier_script, input_file, output_file):
    """
    Verify a solution using the verifier script.
    Returns (is_valid, verified_score, error_message)
    """
    try:
        result = subprocess.run(
            ['python3', verifier_script, input_file, output_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Parse output to get verified score
        if result.returncode == 0:
            # Look for score in output
            for line in result.stdout.split('\n'):
                if 'score' in line.lower() and any(c.isdigit() for c in line):
                    words = line.split()
                    for word in words:
                        if word.isdigit():
                            return True, int(word), None
            return True, 0, "Valid but couldn't parse score"
        else:
            # Extract error message
            error_msg = result.stdout.split('\n')[-1] if result.stdout else result.stderr
            return False, 0, error_msg
    
    except subprocess.TimeoutExpired:
        return False, 0, "Verifier timeout"
    except Exception as e:
        return False, 0, f"Verifier error: {str(e)}"

def run_all_tests(input_dir, output_dir, solver_script, verifier_script=None):
    """
    Run solver on all input files in a directory.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all input files
    input_files = sorted(glob.glob(os.path.join(input_dir, "*.txt")))
    
    if not input_files:
        print(f"No .txt files found in {input_dir}")
        return
    
    print(f"Found {len(input_files)} input files")
    print("=" * 80)
    
    total_score = 0
    valid_count = 0
    invalid_count = 0
    
    results = []
    
    for input_file in input_files:
        base_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, base_name.replace('.txt', '_output.txt'))
        
        print(f"\nProcessing: {base_name}")
        
        # Run solver
        success, score, error = run_solver_on_file(solver_script, input_file, output_file)
        
        if not success:
            print(f"  ✗ Solver failed: {error}")
            invalid_count += 1
            results.append({
                'file': base_name,
                'status': 'SOLVER_FAILED',
                'score': 0,
                'error': error
            })
            continue
        
        print(f"  Solver score: {score}")
        
        # Verify if verifier script is provided
        if verifier_script and os.path.exists(verifier_script):
            is_valid, verified_score, verify_error = verify_solution(
                verifier_script, input_file, output_file
            )
            
            if is_valid:
                print(f"  ✓ Verified: {verified_score}")
                total_score += verified_score
                valid_count += 1
                results.append({
                    'file': base_name,
                    'status': 'VALID',
                    'score': verified_score,
                    'error': None
                })
            else:
                print(f"  ✗ Invalid: {verify_error}")
                invalid_count += 1
                results.append({
                    'file': base_name,
                    'status': 'INVALID',
                    'score': score,
                    'error': verify_error
                })
        else:
            # No verification, just trust the solver output
            print(f"  (not verified)")
            total_score += score
            valid_count += 1
            results.append({
                'file': base_name,
                'status': 'UNVERIFIED',
                'score': score,
                'error': None
            })
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {len(input_files)}")
    print(f"Valid solutions: {valid_count}")
    print(f"Invalid solutions: {invalid_count}")
    print(f"Total score: {total_score}")
    
    if valid_count > 0:
        print(f"Average score: {total_score / valid_count:.2f}")
    
    # Print detailed results
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)
    print(f"{'File':<40} {'Status':<15} {'Score':<10}")
    print("-" * 80)
    
    for result in results:
        status_symbol = {
            'VALID': '✓',
            'INVALID': '✗',
            'UNVERIFIED': '?',
            'SOLVER_FAILED': '✗'
        }.get(result['status'], '?')
        
        print(f"{result['file']:<40} {status_symbol} {result['status']:<13} {result['score']:<10}")
        if result['error']:
            print(f"  Error: {result['error']}")
    
    # Save summary to file
    summary_file = os.path.join(output_dir, 'test_summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f"Total files: {len(input_files)}\n")
        f.write(f"Valid: {valid_count}\n")
        f.write(f"Invalid: {invalid_count}\n")
        f.write(f"Total score: {total_score}\n")
        if valid_count > 0:
            f.write(f"Average score: {total_score / valid_count:.2f}\n")
        f.write("\n")
        for result in results:
            f.write(f"{result['file']}: {result['status']} - {result['score']}\n")
    
    print(f"\nSummary saved to: {summary_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Same Game solver on multiple inputs')
    parser.add_argument('input_dir', help='Directory containing input files')
    parser.add_argument('output_dir', help='Directory to save output files')
    parser.add_argument('--solver', default='solver.py', help='Solver script (default: solver.py)')
    parser.add_argument('--verifier', default=None, help='Verifier script (optional)')
    
    args = parser.parse_args()
    
    # Check if solver exists
    if not os.path.exists(args.solver):
        print(f"Error: Solver script '{args.solver}' not found")
        sys.exit(1)
    
    # Check if verifier exists (if specified)
    if args.verifier and not os.path.exists(args.verifier):
        print(f"Warning: Verifier script '{args.verifier}' not found. Skipping verification.")
        args.verifier = None
    
    # Check if input directory exists
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' not found")
        sys.exit(1)
    
    run_all_tests(args.input_dir, args.output_dir, args.solver, args.verifier)

if __name__ == "__main__":
    main()
