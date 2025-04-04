from flask import Flask, render_template, request, jsonify, redirect, url_for
import yaml
import os
from sensors import read_sensors
from ai_model import predict_adjustment
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_MAP_FILE = "base_map.yaml"

def load_base_map():
    if os.path.exists(BASE_MAP_FILE):
        with open(BASE_MAP_FILE, "r") as f:
            return yaml.safe_load(f)
    else:
        base_map = {"fuel_map": 1.0, "boost_map": 1.0, "lambda_target": 1.0}
        with open(BASE_MAP_FILE, "w") as f:
            yaml.dump(base_map, f)
        return base_map

def save_base_map(base_map):
    with open(BASE_MAP_FILE, "w") as f:
        yaml.dump(base_map, f)

base_map = load_base_map()

@app.route("/")
def index():
    return render_template("index.html", base_map=base_map)

@app.route("/data", methods=["GET"])
def data():
    sensor_data = read_sensors()
    return jsonify({"sensor_data": sensor_data, "base_map": base_map})

@app.route("/update", methods=["POST"])
def update():
    global base_map
    command = request.form.get("command")
    step = 0.01
    if command == "fuel_map_increase":
        base_map["fuel_map"] += step
    elif command == "fuel_map_decrease":
        base_map["fuel_map"] -= step
    elif command == "boost_map_increase":
        base_map["boost_map"] += step
    elif command == "boost_map_decrease":
        base_map["boost_map"] -= step
    elif command == "lambda_target_increase":
        base_map["lambda_target"] += step
    elif command == "lambda_target_decrease":
        base_map["lambda_target"] -= step
    elif command == "simulate_detune":
        base_map["boost_map"] -= step
    elif command == "simulate_aero":
        logger.info("Simulated active aero control event triggered.")
    elif command == "ai_adjust":
        sensor_vals = request.form.getlist("sensor_vals[]")
        try:
            sensor_vals = list(map(float, sensor_vals))
            adjustment = predict_adjustment(sensor_vals)
            if adjustment > 0:
                base_map["fuel_map"] += step
            elif adjustment < 0:
                base_map["fuel_map"] -= step
            logger.info(f"AI predicted adjustment: {adjustment}")
        except Exception as e:
            logger.error(f"Error in AI adjustment: {e}")
    save_base_map(base_map)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)