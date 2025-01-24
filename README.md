Smart Water Management System:
This project implements a Smart Water Management System using MQTT (Message Queuing Telemetry Transport) for communication between components. The system monitors water levels and quality in a main tank and a house tank, controls a water pump, and notifies the user (via a mobile app) of critical conditions.

Features
Water Level Monitoring:

Monitors water levels in the main tank and house tank.

Notifies the user if the house tank water level is below 25%.

Stops the water pump if the main tank water level reaches 99%.

Water Quality Monitoring:

Monitors turbidity in the house tank.

Notifies the user if water quality is low (e.g., turbidity exceeds a threshold).

Pump Control:

Controls the water pump based on water levels in the main tank.

User Notifications:

Sends real-time notifications to the user's mobile app for critical conditions (e.g., low water level, poor water quality).

Sensor Data Request:

Allows the user to request current sensor data (water level, turbidity) from the mobile app.

System Architecture
The system consists of three main components:

Controller:

Connected to sensors (water level, turbidity) and the water pump.

Publishes sensor data to the MQTT broker.

Subscribes to the pump/control topic to receive pump control commands.

Server:

Processes sensor data and checks for critical conditions.

Sends notifications to the user via the user/notifications topic.

Responds to user requests for sensor data via the user/response topic.

User (Mobile App):

Subscribes to the user/notifications topic to receive alerts.

Publishes requests to the user/request topic to fetch current sensor data.

MQTT Topics
The system uses the following MQTT topics for communication:

water_level/main_tank: Publishes the water level of the main tank.

water_level/house_tank: Publishes the water level of the house tank.

water_quality/turbidity: Publishes the turbidity of the water in the house tank.

pump/control: Subscribes to control the water pump.

user/notifications: Publishes notifications to the user.

user/request: User publishes a request for sensor data.

user/response: Server publishes sensor data in response to the request.

How It Works
The controller continuously publishes sensor data (water level, turbidity) to the MQTT broker.

The server processes the sensor data:

Sends notifications to the user if:

The house tank water level is below 25%.

Turbidity exceeds a threshold.

Stops the pump if the main tank water level reaches 99%.

Responds to user requests for sensor data.

The user (mobile app):

Receives notifications for critical conditions.

Requests and displays current sensor data.
