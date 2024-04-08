from time import sleep
from pynput import keyboard
import serial
import threading
# from pyrplidar import PyRPlidar
import math
import numpy as np


import cv2 as cv

# if using the picamera, import those libraries as well
# from picamera.array import PiRGBArray
# from picamera import PiCamera

# point to the haar cascade file in the directory
cascPath = "./haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascPath)

# #start the camera and define settings
# camera = PiCamera()
# camera.resolution = (640, 480)  # a smaller resolution means faster processing
# camera.framerate = 24
# rawCapture = PiRGBArray(camera, size=camera.resolution)

# set the distance between the edge of the screen
# and the borders that trigger robot rotation
side_borders_distance = 150

# face tracking area thresholds are used for forward/backward movement of the robot
# max square area threshold for face tracking
max_face_tracking_width = 150
# min square area threshold for face tracking
min_face_tracking_width = 120

tracked_face_color = (0, 255, 0)
side_border_color = (0, 0, 255)

# Global variables for sensor data
global battery_voltage
global humidity
global temperature

battery_voltage = "N/A"
humidity = "N/A"
temperature = "N/A"

# Global variables for camera angles
global camera_yaw
global camera_pitch

camera_yaw = 90  # Initialize with the camera facing straight forward
camera_pitch = 90  # Initialize with the camera level

ser = serial.Serial('COM9', baudrate=115200, timeout=1)

is_light_on = False


def on_press(key):
    global camera_yaw
    global camera_pitch
    global is_light_on

    try:
        print('alphanumeric key {0} pressed'.format(key.char))

        # Handling alphanumeric keys
        if key.char == 'w':
            print('sent')
            ser.write('motor:forward\n'.encode())
        elif key.char == 'a':
            ser.write('motor:left\n'.encode())
        elif key.char == 's':
            print('sent')
            ser.write('motor:backward\n'.encode())
        elif key.char == 'd':
            print('sent')
            ser.write('motor:right\n'.encode())
        elif key.char == '1':
            print('sent')
            ser.write('motor:speed:50\n'.encode())
        elif key.char == '2':
            print('sent')
            ser.write('motor:speed:100\n'.encode())
        elif key.char == '3':
            print('sent')
            ser.write('motor:speed:150\n'.encode())
        elif key.char == '4':
            print('sent')
            ser.write('motor:speed:200\n'.encode())
        elif key.char == '5':
            print('sent')
            ser.write('motor:speed:255\n'.encode())
        elif key.char == 'p':
            print('sent')
            ser.write('servo:armheight:150\n'.encode())
        elif key.char == 'o':
            print('sent')
            ser.write('servo:armheight:90\n'.encode())
        elif key.char == 'b':
            ser.write('lights:animation:blink_left\n'.encode())
        elif key.char == 'n':
            ser.write('lights:animation:blink_right\n'.encode())
        elif key.char == 'm':
            ser.write('lights:animation:police\n'.encode())
        elif key.char == 'v':
            ser.write('lights:animation:blink_all\n'.encode())
        elif key.char == 'x':
            ser.write('lights:animation:off\n'.encode())
        elif key.char == 'l':
            if is_light_on:
                ser.write('lights:front:0:0:0\n'.encode())
                ser.write('lights:back:0:0:0\n'.encode())
            else:
                ser.write('lights:front:255:255:255\n'.encode())
                ser.write('lights:back:255:255:0\n'.encode())
            is_light_on = not is_light_on

    except AttributeError:
        # Handling arrow keys
        if key == keyboard.Key.left:
            camera_yaw = np.clip(camera_yaw + 10, 0, 180)
            ser.write(f'servo:cam_yaw:{camera_yaw}\n'.encode())
        elif key == keyboard.Key.right:
            camera_yaw = np.clip(camera_yaw - 10, 0, 180)
            ser.write(f'servo:cam_yaw:{camera_yaw}\n'.encode())
        elif key == keyboard.Key.down:
            camera_pitch = np.clip(camera_pitch + 10, 0, 180)
            ser.write(f'servo:cam_pitch:{camera_pitch}\n'.encode())
        elif key == keyboard.Key.up:
            camera_pitch = np.clip(camera_pitch - 10, 0, 180)
            ser.write(f'servo:cam_pitch:{camera_pitch}\n'.encode())


def on_release(key):

    ser.write('motor:stop\n'.encode())

    print('{0} released'.format(
        key))

    if key == keyboard.Key.esc:
        # Stop listener
        quit()
        return False


def draw_camera_fov(frame, yaw, center, fov=60, radius=50, color=(0, 255, 0)):
    # Draw the base circle for the FOV
    cv.circle(frame, center, radius, color, 1)

    # Calculate start and end angles of the FOV
    start_angle = yaw - fov / 2
    end_angle = yaw + fov / 2

    # Define points for the FOV cone
    start_point = (int(center[0] + radius * np.cos(np.radians(start_angle))),
                   int(center[1] - radius * np.sin(np.radians(start_angle))))
    end_point = (int(center[0] + radius * np.cos(np.radians(end_angle))),
                 int(center[1] - radius * np.sin(np.radians(end_angle))))

    # Draw the FOV cone lines
    cv.line(frame, center, start_point, color, 2)
    cv.line(frame, center, end_point, color, 2)


def read_serial_data():
    ser.flushInput()  # Clear the input buffer
    sleep(0.1)

    # Request and read battery voltage
    ser.write('read:battery\n'.encode())
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            if "Battery Voltage:" in line:
                battery_voltage = line.split(":")[1].strip()
                break

    # Request and read DHT data
    ser.write('read:dht\n'.encode())
    humidity, temperature = 'N/A', 'N/A'
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            if "humidity:" in line:
                try:
                    humidity_data, temperature_data = line.split('|')
                    humidity = humidity_data.split(':')[1].strip('%')
                    temperature = temperature_data.split(':')[1].strip('c')
                except ValueError:
                    print("Error parsing DHT data")
                break

    return battery_voltage, humidity, temperature


def opencv_code():
    global battery_voltage
    global humidity
    global temperature
    global camera_yaw

    cap = cv.VideoCapture(0)
    sleep(0.1)
    
    counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get frame dimensions
        height, width = frame.shape[:2]

        counter = counter + 1
        # Read telemetry data (You'll need to define the read_serial_data function)
        if counter > 100:
            counter = 0
            battery_voltage, humidity, temperature = read_serial_data()

        # Display HUD
        cv.putText(frame, f'Battery: {battery_voltage}V', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.putText(frame, f'Humidity: {humidity}%', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.putText(frame, f'Temp: {temperature}C', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw camera FOV
        fov_center = (width - 100, height - 100)  # Position the FOV in the bottom right corner
        draw_camera_fov(frame, camera_yaw, fov_center)

        cv.imshow('Display', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def robot_drive_code():
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()




if __name__ == "__main__":

    thread_robot_control = threading.Thread(target=robot_drive_code)
    thread_opencv = threading.Thread(target=opencv_code)

    thread_opencv.start()
    thread_robot_control.start()
