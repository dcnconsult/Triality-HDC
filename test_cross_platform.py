#!/usr/bin/env python3
"""
Cross-platform compatibility test for Triality-HDC
Tests all major components across different operating systems
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def print_status(test_name, success, details=""):
    """Print test status"""
    status = "[PASS]" if success else "[FAIL]"
    print(f"{test_name:30} {status}")
    if details:
        print(f"{'':32} {details}")

def test_python_environment():
    """Test Python environment and dependencies"""
    print_header("Python Environment Test")
    
    # Python version
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    success = version >= (3, 10)
    print_status("Python Version", success, f"Found: {version_str}, Required: 3.10+")
    
    # Required packages
    required_packages = [
        'numpy', 'scipy', 'matplotlib', 'pandas'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"Package: {package}", True)
        except ImportError:
            print_status(f"Package: {package}", False, "Not installed")
    
    # Virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print_status("Virtual Environment", in_venv, "In venv" if in_venv else "Not in venv")

def test_file_structure():
    """Test project file structure"""
    print_header("File Structure Test")
    
    required_dirs = [
        'core', 'experiments', 'signals', 'hdc', 'hypergraph', 
        'scripts', 'paper', 'results'
    ]
    
    for dir_name in required_dirs:
        exists = os.path.exists(dir_name)
        print_status(f"Directory: {dir_name}", exists)
    
    required_files = [
        'requirements.txt', 'README.md', 'Makefile',
        'run_full_pipeline.bat', 'run_full_pipeline.ps1', 'run_full_pipeline.sh',
        'run_metrics.bat', 'run_metrics.ps1', 'run_metrics.sh',
        'setup.ps1', 'setup.sh'
    ]
    
    for file_name in required_files:
        exists = os.path.exists(file_name)
        print_status(f"File: {file_name}", exists)

def test_scripts_executable():
    """Test if scripts are executable (Unix-like systems)"""
    print_header("Script Executability Test")
    
    if platform.system() in ['Linux', 'Darwin']:  # Unix-like systems
        scripts = ['run_metrics.sh', 'run_full_pipeline.sh', 'setup.sh']
        for script in scripts:
            if os.path.exists(script):
                is_executable = os.access(script, os.X_OK)
                print_status(f"Executable: {script}", is_executable)
            else:
                print_status(f"Executable: {script}", False, "File not found")
    else:
        print_status("Script Executability", True, "Windows - not applicable")

def test_imports():
    """Test module imports"""
    print_header("Module Import Test")
    
    modules_to_test = [
        ('core.triad_hamiltonian', 'simulate_triad'),
        ('signals.bispectrum', 'bicoherence'),
        ('signals.analysis_metrics', 'bicoherence_metrics'),
        ('hypergraph.sl_triad', 'simulate_sl'),
        ('hypergraph.koopman', 'edmd'),
        ('hdc.vsa', 'VSA'),
    ]
    
    for module_name, function_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[function_name])
            has_function = hasattr(module, function_name)
            print_status(f"Import: {module_name}", has_function, 
                        f"Function {function_name}" if has_function else f"Missing {function_name}")
        except ImportError as e:
            print_status(f"Import: {module_name}", False, str(e))

def test_quick_simulation():
    """Test a quick simulation to verify functionality"""
    print_header("Quick Simulation Test")
    
    try:
        from core.triad_hamiltonian import simulate_triad, analytic_signal
        from signals.bispectrum import bicoherence
        
        # Run a very short simulation
        t, Y = simulate_triad(wa=1.0, wb=1.618, wc=2.618, kappa=0.02, tspan=(0, 10))
        a, b, c = analytic_signal(Y)
        B, bic = bicoherence(a.real, b.real, c.real, nperseg=64, noverlap=32)
        
        success = (t is not None and Y is not None and bic is not None)
        print_status("Quick Simulation", success, 
                    f"t={len(t)}, Y={Y.shape}, bic={bic.shape}" if success else "Failed")
        
    except Exception as e:
        print_status("Quick Simulation", False, str(e))

def test_platform_specific():
    """Test platform-specific features"""
    print_header("Platform-Specific Test")
    
    system = platform.system()
    print_status("Platform Detection", True, f"OS: {system}")
    
    # Test appropriate scripts for platform
    if system == "Windows":
        scripts = ['run_full_pipeline.bat', 'run_metrics.bat', 'setup.ps1']
    else:
        scripts = ['run_full_pipeline.sh', 'run_metrics.sh', 'setup.sh']
    
    for script in scripts:
        exists = os.path.exists(script)
        print_status(f"Platform Script: {script}", exists)

def generate_report():
    """Generate a compatibility report"""
    print_header("Compatibility Report")
    
    system_info = {
        "platform": platform.platform(),
        "system": platform.system(),
        "python_version": sys.version,
        "architecture": platform.architecture(),
    }
    
    report = {
        "timestamp": platform.python_compiler(),
        "system_info": system_info,
        "test_results": "See output above"
    }
    
    with open("results/compatibility_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print_status("Report Generated", True, "results/compatibility_report.json")

def main():
    """Run all compatibility tests"""
    print("Triality v2.0 - Cross-Platform Compatibility Test")
    print("=" * 60)
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    # Run all tests
    test_python_environment()
    test_file_structure()
    test_scripts_executable()
    test_imports()
    test_quick_simulation()
    test_platform_specific()
    generate_report()
    
    print_header("Test Complete")
    print("All compatibility tests completed.")
    print("Check results/compatibility_report.json for detailed report.")

if __name__ == "__main__":
    main()
