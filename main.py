from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from plyer import gps
import json
import paho.mqtt.client as mqtt
import time

Window.clearcolor = (1, 1, 1, 1)

# MQTT Broker input fields
MQTT_Broker_helper = """
MDTextField:
    id: broker
    hint_text: "Enter MQTT_Broker IP"
    helper_text: " . "
    helper_text_mode: "on_focus"
    pos_hint: {'center_x': 0.5, 'center_y': 0.95}
    size_hint_x: None
    width: 250
"""

Publisher_name_helper = """
MDTextField:
    id: publisher
    hint_text: "Enter Publisher Name"
    helper_text: " . "
    helper_text_mode: "on_focus"
    pos_hint: {'center_x': 0.5, 'center_y': 0.88}
    size_hint_x: None
    width: 250
"""

ClientID_helper = """
MDTextField:
    id: clientid
    hint_text: "Enter Client ID"
    helper_text: " . "
    helper_text_mode: "on_focus"
    pos_hint: {'center_x': 0.5, 'center_y': 0.81}
    size_hint_x: None
    width: 250
"""

class GPSMQTTApp(MDApp):
    def build(self):
        screen = Screen()
        self.theme_cls.primary_palette = "Green"

        # Load input fields
        self.mqtt_broker = Builder.load_string(MQTT_Broker_helper)
        screen.add_widget(self.mqtt_broker)

        self.publisher_name = Builder.load_string(Publisher_name_helper)
        screen.add_widget(self.publisher_name)

        self.clientID = Builder.load_string(ClientID_helper)
        screen.add_widget(self.clientID)

        # Connect & Disconnect Buttons
        self.connect_btn = MDRectangleFlatButton(
            text='Connect', pos_hint={'center_x': 0.33, 'center_y': 0.72},
            size_hint_x=None, on_release=self.on_connect)
        screen.add_widget(self.connect_btn)

        self.disconnect_btn = MDRectangleFlatButton(
            text='Disconnect', pos_hint={'center_x': 0.66, 'center_y': 0.72},
            size_hint_x=None, on_release=self.on_disconnect)
        screen.add_widget(self.disconnect_btn)

        # LogBox to display location data
        self.logbox = TextInput(
            multiline=True, pos_hint={'center_x': 0.5, 'center_y': 0.43},
            size_hint=(0.85, 0.45), font_size=16,
            background_color=(0.9, 0.9, 0.9, 1), readonly=True
        )
        screen.add_widget(self.logbox)

        # Start & Stop Buttons
        self.start_btn = MDRectangleFlatButton(
            text='Start GPS', pos_hint={'center_x': 0.3, 'center_y': 0.15},
            size_hint_x=None, on_release=self.start_gps)
        screen.add_widget(self.start_btn)

        self.stop_btn = MDRectangleFlatButton(
            text='Stop GPS', pos_hint={'center_x': 0.7, 'center_y': 0.15},
            size_hint_x=None, on_release=self.stop_gps)
        screen.add_widget(self.stop_btn)

        self.mqttc = mqtt.Client()  # MQTT Client
        return screen

    def on_connect(self, instance):
        """ Connect to MQTT broker """
        broker_ip = self.mqtt_broker.text
        publisher_name = self.publisher_name.text
        clientid = self.clientID.text

        if broker_ip and publisher_name and clientid:
            try:
                self.clientid = int(clientid)
                self.publisher_name = publisher_name

                self.mqttc.connect(broker_ip, 1883, 60)
                self.mqttc.loop_start()
                self.logbox.text += f"Connected to MQTT broker {broker_ip} as {publisher_name} (ClientID: {self.clientid})\n"
            except Exception as e:
                self.logbox.text += f"MQTT Connection Failed: {e}\n"
        else:
            self.logbox.text += "Please enter all required fields.\n"

    def on_disconnect(self, instance):
        """ Disconnect from MQTT broker """
        self.mqttc.disconnect()
        self.mqttc.loop_stop()
        self.logbox.text += "Disconnected from MQTT broker.\n"

    def start_gps(self, instance):
        """ Start GPS Tracking """
        self.logbox.text += "Starting GPS...\n"
        try:
            gps.configure(on_location=self.on_gps_update, on_status=self.on_gps_status)
            gps.start(minTime=1000, minDistance=0)  # Fetch every second
        except Exception as e:
            self.logbox.text += f"GPS Start Failed: {e}\n"

    def stop_gps(self, instance):
        """ Stop GPS Tracking """
        self.logbox.text += "Stopping GPS...\n"
        try:
            gps.stop()
        except Exception as e:
            self.logbox.text += f"GPS Stop Failed: {e}\n"

    def on_gps_update(self, **kwargs):
        """ Callback when GPS updates """
        latitude = kwargs.get('lat', 'N/A')
        longitude = kwargs.get('lon', 'N/A')
        altitude = kwargs.get('altitude', 'N/A')
        speed = kwargs.get('speed', 'N/A')
        accuracy = kwargs.get('accuracy', 'N/A')

        timestamp = int(time.time() * 1000)
        loctype = "gps"

        location_text = f"GPS Location:\nLatitude: {latitude}\nLongitude: {longitude}\nAltitude: {altitude}\nSpeed: {speed}\nAccuracy: {accuracy}\n"
        self.logbox.text += location_text

        self.publish_gps_data(loctype, timestamp, latitude, longitude, altitude, speed, accuracy)

    def on_gps_status(self, status):
        """ GPS Status Update """
        self.logbox.text += f"GPS Status: {status}\n"

    def publish_gps_data(self, loctype, timestamp, latitude, longitude, altitude, speed, accuracy):
        """ Publish GPS Data to MQTT Broker """
        payload = {
            "clientid": self.clientid,
            "type": loctype,
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "speed": speed,
            "accuracy": accuracy
        }
        self.mqttc.publish("location", json.dumps(payload))
        print(f"Published: {json.dumps(payload)}")

if __name__ == "__main__":
    GPSMQTTApp().run()

