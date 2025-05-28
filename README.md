![IMG_9863](https://github.com/user-attachments/assets/87c57f40-d9ba-4cc2-a4c4-e14010aea40b)
![IMG_9865](https://github.com/user-attachments/assets/076afd73-ad54-4361-a130-eb2b64f005cf)
![IMG_9852](https://github.com/user-attachments/assets/ee295b81-a82b-4ee5-89d5-ec698ce011ef)

Here is the reformatted Markdown (.md) version of the full technical README for n.Tec-5—FRONT-END. You can copy this directly into your repository’s README.md file:

⸻


# n.Tec-5 Front-End

> A real-time, AI-enhanced vehicle diagnostic and monitoring dashboard built with Flask, CAN-bus integration, TensorFlow, and modular YAML-based configuration.  

---

## 📐 System Architecture

The **n.Tec‑5 Front‑End** is a Flask-based modular UI system for monitoring sensor data from vehicles in real time, powered by CAN-bus protocols and deep learning analytics. It connects to a back-end CAN interface, collects live engine/vehicle telemetry, processes the data via an AI engine, and renders the results as dynamic visualizations.

Core components:

- `Flask` RESTful API
- `python-can` for hardware interface
- `tensorflow` for AI model inference
- `cantools` for decoding CAN messages
- YAML-based sensor configuration and UI mapping

---

## 🧱 Component Breakdown

### `app.py`

- Flask App Factory (`create_app()`)
- Blueprint Registration:
  - `/api` for JSON sensor data
  - `/ui` for HTML UI routes
- Integration of CAN thread & model inference
- Cross-platform WSGI compatibility

### `sensors.py`

- Class: `CanSensor`
- Threaded CAN reading loop
- Uses `python-can` to decode and store sensor packets
- Implements retry mechanism with backoff

### `ai_model.py`

- Loads TensorFlow SavedModel
- Normalizes time-series data
- Outputs classification/prediction metrics
- Model path configurable via YAML

### `base_map.yam`

```yaml
- id: 0x0C
  name: rpm
  unit: rev/min
  scale: 0.25
  offset: 0

	•	Defines:
	•	Sensor mappings
	•	Units
	•	Scaling factors
	•	UI layout
	•	Model hyperparameters

⸻

🖼️ Static Assets & Templates
	•	/templates/index.html: Bootstrap + Jinja2
	•	/static/js/main.js: D3.js for charts + Fetch for JSON polling
	•	/static/css/main.css: Responsive layout

⸻

🧪 Development Setup

Prerequisites

sudo apt install python3-pip can-utils
pip install virtualenv

Virtual Environment

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

CAN Emulator (Linux)

sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0


⸻

📦 Build & Distribution

PyInstaller Build

pyinstaller --clean --onefile app.spec

Produces:
	•	Linux/macOS: dist/ntec5_frontend
	•	Windows: dist/NTec5_FrontEnd.exe

Dockerfile

FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]

docker-compose.yml

version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "5000:5000"
    devices:
      - "/dev/vcan0:/dev/vcan0"
    privileged: true


⸻

⚙️ Runtime Configuration

Env Variables
	•	CAN_CHANNEL=can0
	•	CAN_BITRATE=500000
	•	MODEL_PATH=./models/model

Model Pathing

The model must be saved as a TensorFlow SavedModel directory and defined in base_map.yam.

UI Sections

Each section in YAML maps to a dashboard panel.

⸻

🔧 Code Flow Summary

Request Handling

flowchart TD
  A[Start App] --> B[Init Flask]
  B --> C[Init CAN Thread]
  B --> D[Load Config & Model]
  D --> E[Serve UI + APIs]

Endpoint Routes
	•	/ → HTML dashboard
	•	/api/data → live sensor JSON
	•	/api/predict → AI model results

⸻

🧰 Logging & Error Handling

Custom Exceptions
	•	SensorError
	•	ModelError
	•	ApiError

Logging Format

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


⸻

📊 Performance Profiling
	•	Load Testing: Use locust
	•	Model Profiling: TensorBoard
	•	Python Profiling: py-spy, cProfile

⸻

🛡️ Security Practices
	•	CORS limited to known origins
	•	Secrets/environment via .env or os.environ
	•	Avoid unvalidated JSON inputs
	•	Use HTTPS proxy (e.g., NGINX)

⸻

❓ Troubleshooting

Problem	Cause	Solution
No CAN data	Interface down	sudo ip link set can0 up
UI empty	JS fetch errors	Check browser console
Inference slow	GPU not enabled	Install TensorFlow GPU


⸻

📁 Directory Structure

NTec_Web/
├── app.py
├── ai_model.py
├── base_map.yam
├── sensors.py
├── requirements.txt
├── static/
│   └── js, css
├── templates/
│   └── index.html


⸻

📎 requirements.txt

Flask==2.2.2
python-can==4.2.2
cantools==36.2.0
PyYAML==6.0
tensorflow==2.11.0
gunicorn==20.1.0


⸻

🧬 Appendix

Sample PyInstaller Spec (app.spec)

a = Analysis(['app.py'],
             datas=[('templates/*', 'templates'), ('static/*', 'static')],
             hiddenimports=['can', 'cantools'])


⸻

🚀 CI/CD Setup

You can automate builds using GitHub Actions:

- uses: actions/setup-python@v4
  with:
    python-version: 3.10
- run: pip install -r requirements.txt pyinstaller
- run: pyinstaller app.spec
- uses: actions/upload-artifact@v3
  with:
    path: dist/*


⸻

🏁 Conclusion

This front-end application represents a modular, hardware-integrated, AI-enhanced data visualization system for automotive diagnostics. Its clean architecture, Docker-ready setup, and PyInstaller build support make it ideal for deployment on:
	•	Local dev environments
	•	Raspberry Pi embedded units
	•	Production fleet analytics

For back-end integration, refer to:
n.Tec-5—BACK-END
or the full system:
2JZ-GTE-Predictive-Monitoring-System

⸻

WORK IN PROGRESS BY: H. Pandit

---

Let me know if you’d like the `.md` file itself exported or zipped. I can also generate a matching one for the BACK-END repo.
