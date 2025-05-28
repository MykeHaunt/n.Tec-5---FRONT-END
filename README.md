
# n.Tec-5 Front-End: Technical Documentation

This document provides a comprehensive, end‑to‑end technical specification and usage guide for the **n.Tec‑5 Front‑End** web application. It is structured to match the documentation style of the [2JZ‑GTE Predictive Monitoring System](https://github.com/MykeHaunt/2JZ-GTE-Predictive-Monitoring-System), with detailed information about architecture, build pipelines, deployment, and internal modules.

---

## Table of Contents

1. [System Architecture](#system-architecture)  
2. [Component Breakdown](#component-breakdown)  
   - [Application Entrypoint (`app.py`)](#application-entrypoint-apppy)  
   - [Sensor Interface (`sensors.py`)](#sensor-interface-sensorspy)  
   - [AI Model Wrapper (`ai_model.py`)](#ai-model-wrapper-ai_modelpy)  
   - [Configuration & Mapping (`base_map.yam`)](#configuration--mapping-base_mapyam)  
   - [Static Assets & Templates](#static-assets--templates)  
3. [Development Environment Setup](#development-environment-setup)  
4. [Detailed Installation](#detailed-installation)  
5. [Build & Distribution](#build--distribution)  
6. [Runtime Configuration](#runtime-configuration)  
7. [Code Walkthrough](#code-walkthrough)  
8. [Error Handling & Logging](#error-handling--logging)  
9. [Performance & Profiling](#performance--profiling)  
10. [Security Considerations](#security-considerations)  
11. [Troubleshooting Guide](#troubleshooting-guide)  
12. [Appendices](#appendices)  
    - [Appendix A: Full `requirements.txt`](#appendix-a-full-requirementstxt)  
    - [Appendix B: Sample `docker-compose.yml`](#appendix-b-sample-docker-composeyml)

---

## System Architecture

The n.Tec‑5 Front‑End is a **Flask-based microservice** providing a responsive web interface for visualizing real-time sensor data and model outputs. Key subsystems:

- RESTful Flask API backend  
- CAN bus reader thread using `python-can`  
- AI inference pipeline (TensorFlow)  
- Static configuration (YAML)  
- Web UI using Bootstrap + D3.js  

The system reads sensor values from a CAN interface, buffers the data, passes it to a deep learning model for predictions, and updates the UI in real time using asynchronous fetches and EventSource streams.

---

## Component Breakdown

### Application Entrypoint (`app.py`)

- Flask app factory: `create_app()`  
- Blueprints:
  - `/api` — Sensor data and AI predictions
  - `/ui` — UI template rendering  
- WS integration for streaming updates

### Sensor Interface (`sensors.py`)

- Class: `CanSensor`  
- Interfaces with `python-can`  
- Reads and decodes CAN frames into structured data  
- Runs as a daemon thread  
- Uses `cantools` to parse DBC files  

### AI Model Wrapper (`ai_model.py`)

- Loads TensorFlow SavedModel  
- Preprocessing: Normalization, window slicing  
- Inference: Callable function returning anomaly scores or predictions  
- Designed to support multiple output targets (e.g. heat, pressure)

### Configuration & Mapping (`base_map.yam`)

```yaml
- id: 0x0C
  name: rpm
  unit: rev/min
  scale: 0.25
  offset: 0
```

- Sensor metadata and UI layout  
- Sampling configuration  
- Model normalization stats  

### Static Assets & Templates

- `templates/index.html`: Bootstrap + Jinja2  
- `static/js/main.js`: D3.js + EventSource  
- `static/css/main.css`: Custom layout  

---

## Development Environment Setup

### Versioned Dependencies

- Flask 2.2+  
- python-can 4.2.2+  
- tensorflow 2.11+  
- cantools, PyYAML, gunicorn  

### Virtual Environments

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Local CAN Bus Emulation

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

---

## Detailed Installation

### Initial Clone

```bash
git clone https://github.com/MykeHaunt/n.Tec-5---FRONT-END.git
cd n.Tec-5---FRONT-END/NTec_Web
```

### Directory Layout

```text
├── app.py
├── sensors.py
├── ai_model.py
├── base_map.yam
├── requirements.txt
├── static/
└── templates/
```

### Dependency Installation

```bash
pip install -r requirements.txt
```

---

## Build & Distribution

### PyInstaller

1. Create `app.spec` with templates and static folders included in `datas`.  
2. Build with:

```bash
pyinstaller --clean --onefile app.spec
```

3. Output binary at: `dist/NTec5_FrontEnd.exe` or `dist/ntec5_frontend`

### Dockerization

#### Dockerfile

```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y can-utils
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
```

#### docker-compose.yml

```yaml
version: '3.8'
services:
  frontend:
    build: .
    ports: ["5000:5000"]
    devices:
      - "/dev/vcan0:/dev/vcan0"
    privileged: true
```

### GitHub Actions

CI pipeline runs tests, packages the binary, and pushes artifacts or Docker images to GitHub Packages.

---

## Runtime Configuration

- `CAN_CHANNEL` — Defaults to `can0`  
- `CAN_BITRATE` — Defaults to `500000`  
- `MODEL_PATH` — Path to TensorFlow model  

---

## Code Walkthrough

### `app.py`

- Initializes server  
- Defines `/api/data`, `/api/predict`, `/` routes  
- Injects `base_map` into Jinja templates  

### `sensors.py`

```python
class CanSensor:
    def __init__(self, config):
        self.bus = can.interface.Bus(**config)
        self.buffer = deque(maxlen=config['buffer_size'])
```

- Background thread reads from bus  
- Catches errors and retries with backoff  

### `ai_model.py`

- Loads model only on first call  
- Preprocesses data (normalization, windowing)  
- Returns dictionary of prediction scores  

---

## Error Handling & Logging

### Logging

```python
import logging
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
```

### Exceptions

- `SensorError`  
- `ModelError`  
- `ApiError`  

---

## Performance & Profiling

### Load Testing

```bash
pip install locust
locust -f locustfile.py
```

### Profiling Tools

- `cProfile`  
- `py-spy`  
- TensorBoard  

---

## Security Considerations

- Use HTTPS + reverse proxy in production  
- Sanitize all inputs to `/api/*` routes  
- Restrict CORS origins  
- Set Flask `SECRET_KEY` securely  

---

## Troubleshooting Guide

| Symptom             | Cause                            | Fix                                  |
|---------------------|----------------------------------|--------------------------------------|
| CAN data missing    | Interface not configured         | `ip link set can0 up type can ...`   |
| Model is slow       | TensorFlow batch too large       | Reduce sliding window size           |
| UI crashes          | Invalid YAML or JavaScript bug   | Validate `base_map.yam` and console logs |
| PyInstaller fails   | Missing `static/` or `templates/`| Include in `.spec` file              |

---

## Appendices

### Appendix A: Full `requirements.txt`

```
Flask==2.2.2
python-can==4.2.2
cantools==36.2.0
PyYAML==6.0
tensorflow==2.11.0
gunicorn==20.1.0
```

### Appendix B: Sample `docker-compose.yml`

```yaml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "5000:5000"
    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"
    privileged: true
```

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

## Author

**WORK IN PROGRESS BY: H. Pandit**
