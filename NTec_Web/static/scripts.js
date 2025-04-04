// script.js

// Function to periodically fetch sensor data and update the dashboard.
function fetchData() {
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        document.getElementById("steering").innerText = data.sensor_data.steering_angle;
        document.getElementById("throttle").innerText = data.sensor_data.throttle_position;
        document.getElementById("brake").innerText = data.sensor_data.brake_pressure;
        document.getElementById("lambda").innerText = data.sensor_data.lambda_sensor;
        document.getElementById("rpm").innerText = data.sensor_data.engine_rpm;
        document.getElementById("speed").innerText = data.sensor_data.vehicle_speed;
        document.getElementById("fuel_map").innerText = data.base_map.fuel_map;
        document.getElementById("boost_map").innerText = data.base_map.boost_map;
        document.getElementById("lambda_target").innerText = data.base_map.lambda_target;
    })
    .catch(error => console.error("Error fetching sensor data:", error));
}

// Update sensor data every 2 seconds.
setInterval(fetchData, 2000);