#!/bin/bash

VENV_DIR="rb_venv"
PYTHON_VERSION="python3.12" 

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment with $PYTHON_VERSION..."
  $PYTHON_VERSION -m venv $VENV_DIR
else
  echo "Virtual environment already exists."
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
pip install --upgrade pip

# Get installed packages
installed_packages=$(pip list --format=freeze | cut -d '=' -f 1 | tr 'A-Z' 'a-z')

# Prepare list of missing packages
missing_packages=()

while IFS= read -r line
do
  # Ignore comments and empty lines in requirements.txt
  if [[ "$line" =~ ^#.*$ ]] || [[ -z "$line" ]]; then
    continue
  fi

  # Extract package name without version (handles e.g. package==1.2.3)
  pkg_name=$(echo "$line" | cut -d '=' -f 1 | tr 'A-Z' 'a-z')

  # Check if package is installed
  if ! echo "$installed_packages" | grep -q "^${pkg_name}$"; then
    missing_packages+=("$line")
  fi
done < requirements.txt

# Install missing packages if any
if [ ${#missing_packages[@]} -eq 0 ]; then
  echo "All required packages are already installed."
else
  echo "Installing missing packages: ${missing_packages[*]}"
  pip install "${missing_packages[@]}"
fi

echo "Setup complete. Virtual environment is activated."
echo "To activate it later, run: source $VENV_DIR/bin/activate"
