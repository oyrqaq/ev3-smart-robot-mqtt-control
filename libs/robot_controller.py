import ev3dev.ev3 as ev3
import math
import time

class Snatch3r:
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        self.running = True
        
        try:
            self.pixy = ev3.Sensor(driver_name="pixy-lego")
        except:
            self.pixy = None
        
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.color_sensor.connected
        assert self.ir_sensor.connected

    def forward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def back(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def left(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def right(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()
        
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range, 
            speed_sp=900,
            stop_action=ev3.Motor.STOP_ACTION_BRAKE
        )
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def drive_inches(self, inches_target, speed_deg_per_second):
        position = inches_target * 90
        self.left_motor.run_to_rel_pos(
            position_sp=position, 
            speed_sp=speed_deg_per_second,
            stop_action='brake'
        )
        self.right_motor.run_to_rel_pos(
            position_sp=position, 
            speed_sp=speed_deg_per_second,
            stop_action='brake'
        )
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        motor_degrees = degrees_to_turn * 470 / 90
        self.left_motor.run_to_rel_pos(
            position_sp=motor_degrees,
            speed_sp=turn_speed_sp,
            stop_action='brake'
        )
        self.right_motor.run_to_rel_pos(
            position_sp=-motor_degrees,
            speed_sp=turn_speed_sp,
            stop_action='brake'
        )
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def seek_beacon(self):
        forward_speed = 300
        turn_speed = 100
        
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            
            if current_distance == -128:
                self.stop()
                continue
                
            if math.fabs(current_heading) < 2:
                if current_distance == 0:
                    self.stop()
                    return True
                if current_distance > 0:
                    self.forward(forward_speed, forward_speed)
                    
            elif math.fabs(current_heading) < 10:
                if current_heading < 0:
                    self.left(turn_speed, turn_speed)
                else:
                    self.right(turn_speed, turn_speed)
            else:
                self.stop()
                
            time.sleep(0.2)
            
        self.stop()
        return False

    def follow_line(self, speed=400):
        target = 50
        while self.running:
            value = self.color_sensor.reflected_light_intensity
            error = target - value
            correction = error * 2
            
            left_speed = speed + correction
            right_speed = speed - correction
            
            self.left_motor.run_forever(speed_sp=left_speed)
            self.right_motor.run_forever(speed_sp=right_speed)
            
            if self.touch_sensor.is_pressed:
                break
                
            time.sleep(0.01)
        
        self.stop()

    def loop_forever(self):
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        self.stop()
        self.arm_motor.stop(stop_action='brake')
        self.running = False
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Sound.speak("Goodbye").wait()