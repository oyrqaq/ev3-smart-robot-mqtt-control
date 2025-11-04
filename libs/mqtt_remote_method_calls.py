import json
import collections
import paho.mqtt.client as mqtt

LEGO_NUMBER = 11

class MqttClient:
    def __init__(self, delegate=None):
        self.client = mqtt.Client()
        self.delegate = delegate
        self.subscription_topic_name = None
        self.publish_topic_name = None

    def connect_to_ev3(self, mqtt_broker_ip_address="mosquitto.csse.rose-hulman.edu", lego_robot_number=LEGO_NUMBER):
        self.connect("msg4pc", "msg4ev3", mqtt_broker_ip_address, lego_robot_number)

    def connect_to_pc(self, mqtt_broker_ip_address="mosquitto.csse.rose-hulman.edu", lego_robot_number=LEGO_NUMBER):
        self.connect("msg4ev3", "msg4pc", mqtt_broker_ip_address, lego_robot_number)

    def connect(self, subscription_suffix, publish_suffix, mqtt_broker_ip_address="mosquitto.csse.rose-hulman.edu", lego_robot_number=LEGO_NUMBER):
        lego_name = "lego" + str(lego_robot_number).zfill(2)
        self.subscription_topic_name = lego_name + "/" + subscription_suffix
        self.publish_topic_name = lego_name + "/" + publish_suffix
        self.client.on_connect = self._on_connect
        self.client.message_callback_add(self.subscription_topic_name, self._on_message)
        self.client.connect(mqtt_broker_ip_address, 1883, 60)
        print("Connecting to mqtt broker {}".format(mqtt_broker_ip_address), end="")
        self.client.loop_start()

    def send_message(self, function_name, parameter_list=None):
        message_dict = {"type": function_name}
        if parameter_list:
            if isinstance(parameter_list, collections.Iterable):
                message_dict["payload"] = parameter_list
            else:
                message_dict["payload"] = [parameter_list]
        message = json.dumps(message_dict)
        self.client.publish(self.publish_topic_name, message)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(" ... Connected!")
        else:
            print(" ... Error!!!")
            exit()
        print("Publishing to topic:", self.publish_topic_name)
        self.client.on_subscribe = self._on_subscribe
        self.client.subscribe(self.subscription_topic_name)

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed to topic:", self.subscription_topic_name)

    def _on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        if not self.delegate:
            print("Missing a delegate")
            return

        try:
            message_dict = json.loads(message)
        except ValueError:
            print("Unable to decode the received message as JSON")
            return

        if "type" not in message_dict:
            print("Received a messages without a 'type' parameter.")
            return
            
        message_type = message_dict["type"]
        if hasattr(self.delegate, message_type):
            method_to_call = getattr(self.delegate, message_type)
            if "payload" in message_dict:
                message_payload = message_dict["payload"]
                method_to_call(*message_payload)
            else:
                method_to_call()

    def close(self):
        self.delegate = None
        self.client.loop_stop()
        self.client.disconnect()