import libs.mqtt_remote_method_calls as com
import libs.robot_controller as robo

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

if __name__ == "__main__":
    main()