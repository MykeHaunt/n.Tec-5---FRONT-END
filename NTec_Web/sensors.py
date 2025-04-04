import random
import logging

logger = logging.getLogger(__name__)

try:
    import can
except ImportError:
    can = None

def read_sensors():
    """
    Reads sensor data from a CAN interface if available,
    otherwise returns simulated sensor data.
    """
    sensor_data = {}
    if can:
        try:
            # Example: setup a CAN bus interface.
            bus = can.interface.Bus(channel='can0', bustype='socketcan')
            message = bus.recv(timeout=1.0)
            if message:
                # Parse message data as needed.
                sensor_data = {
                    "steering_angle": float(message.data[0]) / 255,
                    "throttle_position": float(message.data[1]) / 255,
                    "brake_pressure": float(message.data[2]) / 255,
                    "lambda_sensor": float(message.data[3]) / 255,
                    "engine_rpm": int(message.data[4]),
                    "vehicle_speed": int(message.data[5])
                }
            else:
                sensor_data = _simulate_sensor_data()
        except Exception as e:
            logger.error(f"Error reading CAN data: {e}")
            sensor_data = _simulate_sensor_data()
    else:
        sensor_data = _simulate_sensor_data()
    return sensor_data

def _simulate_sensor_data():
    """
    Returns simulated sensor data.
    """
    return {
        "steering_angle": round(random.uniform(-1, 1), 2),
        "throttle_position": round(random.uniform(0, 1), 2),
        "brake_pressure": round(random.uniform(0, 1), 2),
        "lambda_sensor": round(random.uniform(0.9, 1.1), 2),
        "engine_rpm": random.randint(800, 7000),
        "vehicle_speed": random.randint(0, 150)
    }