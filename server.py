import paho.mqtt.client as mqtt

# MQTT Broker details
broker = "mqtt.eclipseprojects.io"
port = 1883
client_id = "server"

# Store latest sensor data
latest_sensor_data = {
    "main_tank_level": 0,
    "house_tank_level": 0,
    "turbidity": 0,
}

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Server connected to MQTT Broker")
    client.subscribe("water_level/main_tank")
    client.subscribe("water_level/house_tank")
    client.subscribe("water_quality/turbidity")
    client.subscribe("user/request")  # Subscribe to user request topic

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()  # Decode payload as string

    if topic == "user/request":
        # Handle user request for sensor data
        if payload == "get_sensor_data":
            response = f"""
            Main Tank Level: {latest_sensor_data["main_tank_level"]}%
            House Tank Level: {latest_sensor_data["house_tank_level"]}%
            Turbidity: {latest_sensor_data["turbidity"]} NTU
            """
            client.publish("user/response", response)
    else:
        # Handle sensor data updates
        try:
            payload = float(payload)  # Convert payload to float for sensor data
            if topic == "water_level/main_tank":
                latest_sensor_data["main_tank_level"] = payload
                if payload >= 99:
                    print("Main tank is full. Stopping pump.")
                    client.publish("pump/control", "stop")
            elif topic == "water_level/house_tank":
                latest_sensor_data["house_tank_level"] = payload
                if payload < 25:
                    print("House tank water level is below 25%. Notifying user to reduce usage.")
                    client.publish("user/notifications", "House tank water level is below 25%. Reduce usage.")
            elif topic == "water_quality/turbidity":
                latest_sensor_data["turbidity"] = payload
                if payload > 50:  # Example turbidity threshold
                    print("Water quality is low (turbidity). Notifying user.")
                    client.publish("user/notifications", "Water quality is low (turbidity). Check water supply.")
        except ValueError:
            print(f"Invalid payload received on topic {topic}: {payload}")

# Initialize MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker, port, 60)

# Keep the server running
client.loop_forever()