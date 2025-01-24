import paho.mqtt.client as mqtt

# MQTT Broker details
broker = "mqtt.eclipseprojects.io"
port = 1883
client_id = "user_mobile"

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("User connected to MQTT Broker")
    client.subscribe("user/notifications")
    client.subscribe("user/response")  # Subscribe to response topic

def on_message(client, userdata, msg):
    if msg.topic == "user/notifications":
        print(f"Notification received: {msg.payload.decode()}")
    elif msg.topic == "user/response":
        print(f"Sensor Data Received:\n{msg.payload.decode()}")

# Initialize MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker, port, 60)

# Keep the user device running
client.loop_start()

# Simulate user requesting sensor data
while True:
    user_input = input("Press 'R' to request sensor data or 'Q' to quit: ").strip().upper()
    if user_input == "R":
        print("Requesting sensor data...")
        client.publish("user/request", "get_sensor_data")
    elif user_input == "Q":
        break

















        