import paho.mqtt.client as mqtt
import os
import logging

# Config logging
logging.basicConfig(level=logging.INFO)

# This implementation is probably not great. Since the loops in run.py. Will maybe refactor this later. Or not.
class MQTTClient:
    def __init__(self):
        self.mqtt_client = None
        self.mqtt_connected = False
        self.mqtt_message_sent = False
        self.mqtt_host = os.getenv('MQTT_HOST')
        self.mqtt_port = int(os.getenv('MQTT_PORT', 1883))  # Ensure port is an integer
        self.mqtt_username = os.getenv('MQTT_USERNAME')
        self.mqtt_password = os.getenv('MQTT_PASSWORD')
        self.mqtt_topic = os.getenv('MQTT_TOPIC', 'expoapi-bridge')
        self.setup_mqtt()

    def setup_mqtt(self):
        # Make a check that the variables are not empty
        if not self.mqtt_host or not self.mqtt_port or not self.mqtt_username or not self.mqtt_password:
            missing_variables = []
            if not self.mqtt_host:
                missing_variables.append("MQTT_HOST")
            if not self.mqtt_port:
                missing_variables.append("MQTT_PORT")
            if not self.mqtt_username:
                missing_variables.append("MQTT_USERNAME")
            if not self.mqtt_password:
                missing_variables.append("MQTT_PASSWORD")
            error_message = "Missing MQTT environment variables: " + ", ".join(missing_variables)
            logging.error(error_message)
        else:
            try:
                # Setup the MQTT client
                self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
                # Bind the on_connect function to the client
                self.mqtt_client.on_connect = self.on_connect
                self.mqtt_client.on_connect_fail = self.on_connect_fail
                self.mqtt_client.on_disconnect = self.on_disconnect
                self.mqtt_client.on_publish = self.on_publish_callback
                self.mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
                logging.info("Trying to connect to MQTT broker... Host: {}, Port: {}".format(self.mqtt_host, self.mqtt_port))
                self.mqtt_client.connect(self.mqtt_host, self.mqtt_port)
                self.mqtt_client.loop_start()  # Start the loop in a separate thread
            except Exception as e:
                logging.error(f"Failed to connect to MQTT broker: {e}")

    def on_connect(self, client, userdata, flags, reason_code, properties):
        logging.info(f"MQTT Connected with result code {reason_code}")
        self.mqtt_connected = True

    def on_connect_fail(self, client, userdata):
        logging.error(f"MQTT Connection failed")
        self.mqtt_connected = False

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        logging.info(f"MQTT Disconnected with result code {reason_code}")
        self.mqtt_connected = False

    def publish(self, topic_subpath, message):
        if self.mqtt_connected:
            logging.info("Publishing message to MQTT broker...")
            self.mqtt_client.publish(self.mqtt_topic + "/" + topic_subpath, message, retain=True)
        else:
            logging.error("Cannot publish message. MQTT client is not connected.")
            self.mqtt_message_sent = True

    def on_publish_callback(self, client, userdata, mid, reason_code, properties):
        self.mqtt_message_sent = True
        logging.info(f"Message published with mid: {mid} and reason code: {reason_code}")

    def disconnect(self):
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()