#!/bin/bash
# Cross-platform setup script for Triality-HDC
# Detects OS and sets up environment appropriately

echo "Triality v2.0 - Cross-Platform Setup"
echo "===================================="

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    echo "Warning: Unknown OS type: $OSTYPE"
    OS="unknown"
fi

echo "Detected OS: $OS"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python not found. Please install Python 3.10+ first."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Activating..."
else
    $PYTHON_CMD -m venv .venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ "$OS" == "windows" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install requirements
echo ""
echo "Installing requirements..."
pip install -r requirements.txt

# Make scripts executable (Unix-like systems)
if [ "$OS" != "windows" ]; then
    echo ""
    echo "Making scripts executable..."
    chmod +x run_metrics.sh run_full_pipeline.sh setup.sh
fi

# Create results directory
echo ""
echo "Creating results directory..."
mkdir -p results

echo ""
echo "======================================="
echo "Setup completed successfully!"
echo ""
echo "To run the full pipeline:"
if [ "$OS" == "windows" ]; then
    echo "  Windows: .\\run_full_pipeline.bat"
    echo "  PowerShell: .\\run_full_pipeline.ps1"
else
    echo "  Unix/Linux/macOS: ./run_full_pipeline.sh"
    echo "  Makefile: make full"
fi
echo ""
echo "To run individual components:"
if [ "$OS" == "windows" ]; then
    echo "  Metrics only: .\\run_metrics.bat"
    echo "  PowerShell: .\\run_metrics.ps1"
else
    echo "  Metrics only: ./run_metrics.sh"
    echo "  Makefile: make all"
fi
echo "======================================="
