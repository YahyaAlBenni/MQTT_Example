import paho.mqtt.client as mqtt
import random
import time

# MQTT Broker details
broker = "mqtt.eclipseprojects.io"
port = 1883
client_id = "controller"

# Sensor data simulation
def simulate_sensor_data():
    main_tank_level = random.randint(0, 100)  # Simulate main tank water level (0-100%)
    house_tank_level = random.randint(0, 100)  # Simulate house tank water level (0-100%)
    turbidity = random.uniform(0, 100)  # Simulate turbidity (0-100 NTU)
    return main_tank_level, house_tank_level, turbidity

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Controller connected to MQTT Broker")
    client.subscribe("pump/control")  # Subscribe to pump control topic

def on_message(client, userdata, msg):
    if msg.topic == "pump/control":
        print(f"Pump control command: {msg.payload.decode()}")

# Initialize MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker, port, 60)

# Main loop
while True:
    main_tank_level, house_tank_level, turbidity = simulate_sensor_data()

    # Publish sensor data
    client.publish("water_level/main_tank", main_tank_level)
    client.publish("water_level/house_tank", house_tank_level)
    client.publish("water_quality/turbidity", turbidity)

    # Check main tank level and stop pump if 99%
    if main_tank_level >= 99:
        client.publish("pump/control", "stop")

    time.sleep(5)  # Simulate sensor data every 5 seconds