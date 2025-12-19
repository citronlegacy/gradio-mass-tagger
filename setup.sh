#!/bin/bash

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt


# Clone the repository (if not already exists)
if [ ! -d "sd-scripts" ]; then
    git clone https://github.com/kohya-ss/sd-scripts.git
else
    echo "sd-scripts directory already exists, skipping clone."
fi

# Navigate into the cloned directory
cd sd-scripts

# Apply patches to requirements.txt
# Uncomment onnx and onnxruntime
sed -i 's/# onnx==1.15.0/onnx==1.15.0/' requirements.txt
sed -i 's/# onnxruntime==1.17.1/onnxruntime==1.17.1/' requirements.txt

# Add torchvision if not already present
if ! grep -q '^torchvision$' requirements.txt; then
    echo 'torchvision' >> requirements.txt
fi

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

echo "Setup complete. The sd-scripts application is ready in the sd-scripts directory. Make sure you have sufficient disk space (~2GB for the WD14 model cache)"