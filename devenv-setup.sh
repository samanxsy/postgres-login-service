#!/bin/bash

echo "*** LETS GET STARTED ***"
sleep 1
# Check if virtualenv is installed
if ! [ -x "$(command -v virtualenv)" ]; then
  echo 'Virtualenv is not installed.' >&2
  echo "Installing virtaulenv..."
    pip install virtualenv
fi

# Create a virtual environment
virtualenv .venv

# Activate the virtual environment
source .venv/bin/activate
sleep 1
echo "Virtual environment activated!"

# Upgrade the pip
echo "Upgrading pip..."
pip install --upgrade pip
sleep 1
# Install the requirements
echo "Installing requirements..."
pip install -r requirements.txt
sleep 2
# Update the requirements list with new dependencies
echo "Updating requirements.txt..."
pip freeze > requirements.txt

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "+++++++++++++++++++++ Setup completed!! ++++++++++++++++++++++++"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo "Activate the virtual environment with: source .venv/bin/activate"
