#!/bin/bash
# Run "source setup.sh" to install dependencies

# Find out if pip or pip3 should be used
if [ -x "$(command -v pip3)" ]; then
    echo "Using pip3"
    PIP=pip3
elif [ -x "$(command -v pip)" ]; then
    echo "Using pip"
    PIP=pip
else
    echo "No pip or pip3 found. Please install pip3."
    exit 1
fi

# If --venv=false is passed, don't use a virtual environment
if [ "$1" = "--venv=false" ]; then
    echo "Not using virtual environment"
else
    # Create virtual environment if it doesn't exist
    $PIP install virtualenv
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment"
        virtualenv venv
    else
        echo "Virtual environment already exists"
    fi
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependecies"
$PIP install -r requirements.txt