import tensorflow as tf
import numpy as np
import logging

logger = logging.getLogger(__name__)

def build_model(input_dim=6):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='tanh')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_model(input_dim=6)

def predict_adjustment(sensor_data):
    if len(sensor_data) != 6:
        logger.error("Expected 6 sensor values for prediction.")
        return 0
    data = np.array(sensor_data).reshape(1, -1)
    prediction = model.predict(data)[0][0]
    if prediction > 0.1:
        return 1
    elif prediction < -0.1:
        return -1
    else:
        return 0