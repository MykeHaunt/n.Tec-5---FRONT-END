---

### quick_start.sh

```bash
#!/bin/bash
# Quick start script for NTec_Web

echo "====================================="
echo "NTec Web Interface Quick Start"
echo "====================================="
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Please check your Python and pip installation."
    exit 1
fi

echo "Dependencies installed successfully."
echo "Starting NTec Web Application..."
python app.py