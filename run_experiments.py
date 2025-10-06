#!/usr/bin/env python3
"""
Convenience script to run all Triality experiments.
Run from the project root directory.
"""

import subprocess
import sys
import os

def run_experiment(module_name, description):
    """Run an experiment module and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Module: {module_name}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, '-m', module_name], 
                              capture_output=True, text=True, check=True)
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print("[SUCCESS]")
        return True
    except subprocess.CalledProcessError as e:
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        print("[FAILED]")
        return False

def main():
    """Run all experiments."""
    print("Triality v2.0 - Running All Experiments")
    print("=" * 60)
    
    # Ensure we're in the right directory
    if not os.path.exists('core') or not os.path.exists('experiments'):
        print("[ERROR] Please run this script from the project root directory")
        print("   Expected structure: core/, experiments/, signals/, etc.")
        sys.exit(1)
    
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    
    experiments = [
        ('experiments.triad_sweep_phi', 'phi-step triad sweep simulation and bicoherence'),
        ('experiments.hypergraph_limit', 'Triadic hypergraph couplings and Koopman spectrum'),
        ('experiments.retuning_latency', 'Retuning latency vs ladder distance analysis'),
    ]
    
    results = []
    for module, description in experiments:
        success = run_experiment(module, description)
        results.append((module, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("EXPERIMENT SUMMARY")
    print('='*60)
    
    for module, success in results:
        status = "[PASSED]" if success else "[FAILED]"
        print(f"{module:30} {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nOverall: {passed}/{total} experiments passed")
    
    if passed == total:
        print("[SUCCESS] All experiments completed successfully!")
        print("Check the 'results/' directory for generated figures.")
    else:
        print("[WARNING] Some experiments failed. Check the output above for details.")
        sys.exit(1)

if __name__ == '__main__':
    main()
