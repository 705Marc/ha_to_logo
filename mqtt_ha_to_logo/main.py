import json
import paho.mqtt.client as mqtt
import time
import os

# Optionens-Datei von Home Assistant Add-ons auslesen
OPTIONS_FILE = "/data/options.json"

broker = os.getenv("MQTT_BROKER", "localhost")
port = int(os.getenv("MQTT_PORT", 1883))
user = os.getenv("MQTT_USER", "")
password = os.getenv("MQTT_PASSWORD", "")

if os.path.exists(OPTIONS_FILE):
    try:
        with open(OPTIONS_FILE, "r") as f:
            options = json.load(f)
            if options.get("mqtt_broker") != "auto":
                broker = options.get("mqtt_broker", broker)
                port = int(options.get("mqtt_port", port))
                user = options.get("mqtt_user", user)
                password = options.get("mqtt_password", password)
    except Exception as e:
        print(f"Fehler beim Lesen der options.json: {e}")

# Automatisches Auslesen des HA Mosquitto Service, falls "auto" gewählt wurde
if broker == "auto":
    broker = os.getenv("MQTT_HOST", "core-mosquitto")
    port = int(os.getenv("MQTT_PORT", 1883))
    user = os.getenv("MQTT_USER", user)
    password = os.getenv("MQTT_PASSWORD", password)

TOPIC = "devices/logo/"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="MQTT_HA_TO_LOGO")

if user and password:
    client.username_pw_set(user, password)
else:
    print("WARNUNG: Keine MQTT-Credentials gefunden oder gesetzt!")

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Erfolgreich mit dem MQTT-Broker verbunden!")
        client.subscribe(TOPIC + "convertHAtoLOGO/#")
    else:
        print(f"Verbindung fehlgeschlagen! Return Code: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        topicTOlogo = msg.topic.replace("convertHAtoLOGO/", "")
        state_content = data.get("state", {})

        for device_name, nested_dict in state_content.items():
            current_value = nested_dict.get("value")
            valueTemplate = {"state": {device_name: {"value": current_value}}}

            match current_value:
                case "Button":
                    print(f"Aktion für {device_name}: Button gedrückt")
                    valueTemplate["state"][device_name]["value"] = [1]
                    client.publish(topicTOlogo, json.dumps(valueTemplate))
                    time.sleep(0.5)
                    valueTemplate["state"][device_name]["value"] = [0]
                    client.publish(topicTOlogo, json.dumps(valueTemplate))

                case "ON":
                    print(f"{device_name} wird dauerhaft eingeschaltet")
                    valueTemplate["state"][device_name]["value"] = [1]
                    client.publish(topicTOlogo, json.dumps(valueTemplate))

                case "OFF":
                    print(f"{device_name} wird ausgeschaltet")
                    valueTemplate["state"][device_name]["value"] = [0]
                    client.publish(topicTOlogo, json.dumps(valueTemplate))

                case _:
                    print(f"Unbekannter Wert für {device_name}: {current_value}")

    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")

client.on_connect = on_connect
client.on_message = on_message

print(f"Verbinde zu Broker {broker}:{port}...")

try:
    client.connect(broker, port, 60)
    client.loop_forever()
except Exception as e:
    print(f"Fehler beim Verbinden: {e}")