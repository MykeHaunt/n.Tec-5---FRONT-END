import tensorflow as tf
import numpy as np
import logging

logger = logging.getLogger(__name__)

# For demonstration purposes, we build a simple model.
# In production, you would load a pretrained model.
def build_model(input_dim=6):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='tanh')  # Output: adjustment direction
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Create a global model instance (in production, load weights from a file)
model = build_model(input_dim=6)

def predict_adjustment(sensor_data):
    """
    Predicts an adjustment direction based on sensor data.
    :param sensor_data: List of sensor values.
    :return: +1 (increase), -1 (decrease), or 0 (no change)
    """
    # Ensure sensor_data has 6 values: steering, throttle, brake, lambda, rpm, speed.
    if len(sensor_data) != 6:
        logger.error("Expected 6 sensor values for prediction.")
        return 0
    data = np.array(sensor_data).reshape(1, -1)
    prediction = model.predict(data)[0][0]
    # Use thresholds to decide adjustment.
    if prediction > 0.1:
        return 1
    elif prediction < -0.1:
        return -1
    else:
        return 0