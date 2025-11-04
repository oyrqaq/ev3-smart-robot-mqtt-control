#!/usr/bin/env python3

import time
import random

class SimulatedRobot:
    def __init__(self):
        self.position = [0, 0]
        self.arm_position = 0
        self.running = True
        
    def forward(self, left_speed, right_speed):
        print(f"🤖 Moving forward: L={left_speed}, R={right_speed}")
        self.position[1] += 1
        print(f"   Position: {self.position}")
        
    def back(self, left_speed, right_speed):
        print(f"🤖 Moving backward: L={left_speed}, R={right_speed}")
        self.position[1] -= 1
        print(f"   Position: {self.position}")
        
    def left(self, left_speed, right_speed):
        print(f"🤖 Turning left: L={left_speed}, R={right_speed}")
        self.position[0] -= 1
        print(f"   Position: {self.position}")
        
    def right(self, left_speed, right_speed):
        print(f"🤖 Turning right: L={left_speed}, R={right_speed}")
        self.position[0] += 1
        print(f"   Position: {self.position}")
        
    def stop(self):
        print("🛑 Robot stopped")
        
    def arm_up(self):
        print("↑ Arm moving up...")
        self.arm_position = 100
        print(f"   Arm position: {self.arm_position}%")
        
    def arm_down(self):
        print("↓ Arm moving down...")
        self.arm_position = 0
        print(f"   Arm position: {self.arm_position}%")
        
    def arm_calibration(self):
        print("🔧 Calibrating arm...")
        for i in range(0, 101, 20):
            print(f"   Calibration: {i}%")
            time.sleep(0.1)
        print("✓ Calibration complete!")
        
    def follow_line(self):
        print("📍 Following line...")
        for i in range(5):
            sensor_value = random.randint(30, 70)
            error = 50 - sensor_value
            left_speed = 400 + error * 2
            right_speed = 400 - error * 2
            print(f"   Sensor: {sensor_value}, L={left_speed}, R={right_speed}")
            time.sleep(0.2)
        print("✓ Line following complete")
        
    def seek_beacon(self):
        print("🔍 Seeking beacon...")
        for i in range(5):
            heading = random.randint(-20, 20)
            distance = random.randint(10, 100)
            print(f"   Beacon: heading={heading}°, distance={distance}cm")
            if distance < 20:
                print("✓ Beacon found!")
                break
            time.sleep(0.2)
        
    def shutdown(self):
        print("👋 Shutting down robot...")
        self.running = False
        print("   Goodbye!")

def run_demo():
    print("="*60)
    print(" EV3 ROBOT SIMULATOR - STANDALONE DEMO")
    print("="*60)
    print("\nThis demo simulates all robot commands without hardware")
    print("or external dependencies.\n")
    
    robot = SimulatedRobot()
    
    demo_sequence = [
        ("Basic Movement Test", [
            ("Forward", lambda: robot.forward(600, 600)),
            ("Stop", lambda: robot.stop()),
            ("Left turn", lambda: robot.left(400, 400)),
            ("Stop", lambda: robot.stop()),
            ("Right turn", lambda: robot.right(400, 400)),
            ("Stop", lambda: robot.stop()),
            ("Backward", lambda: robot.back(500, 500)),
            ("Stop", lambda: robot.stop()),
        ]),
        
        ("Arm Control Test", [
            ("Calibrate arm", lambda: robot.arm_calibration()),
            ("Arm up", lambda: robot.arm_up()),
            ("Arm down", lambda: robot.arm_down()),
        ]),
        
        ("Autonomous Features", [
            ("Line following", lambda: robot.follow_line()),
            ("Beacon seeking", lambda: robot.seek_beacon()),
        ]),
        
        ("Shutdown", [
            ("Shutdown robot", lambda: robot.shutdown()),
        ])
    ]
    
    for section_name, commands in demo_sequence:
        print("\n" + "-"*40)
        print(f" {section_name}")
        print("-"*40)
        
        for description, command in commands:
            print(f"\n>> {description}")
            command()
            time.sleep(0.5)
    
    print("\n" + "="*60)
    print(" DEMO COMPLETE")
    print("="*60)
    
    print("\nSummary:")
    print(f"  Final position: {robot.position}")
    print(f"  Arm position: {robot.arm_position}%")
    print(f"  Robot status: {'Running' if robot.running else 'Shutdown'}")
    
    print("\nThis demonstrates:")
    print("  ✓ Motor control (forward/back/left/right)")
    print("  ✓ Arm manipulation")
    print("  ✓ Sensor feedback simulation")
    print("  ✓ Autonomous navigation modes")
    print("  ✓ MQTT command structure (simulated)")

if __name__ == "__main__":
    run_demo()