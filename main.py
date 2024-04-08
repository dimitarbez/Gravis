import math
import numpy as np
import cv2 as cv
import serial
from time import sleep
import threading
from pynput import keyboard
from pyrplidar import PyRPlidar
from picamera.array import PiRGBArray
from picamera import PiCamera

# Haar cascade file for face detection
cascPath = "./haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascPath)

# Global variables
global battery_voltage, humidity, temperature, camera_yaw, camera_pitch, is_light_on
battery_voltage, humidity, temperature = "N/A", "N/A", "N/A"
camera_yaw, camera_pitch = 90, 90
is_light_on = False

# Serial connection
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

def on_press(key):
    global camera_yaw, camera_pitch, is_light_on
    try:
        handle_alphanumeric_key(key)
    except AttributeError:
        handle_arrow_key(key)

def handle_alphanumeric_key(key):
    if key.char in ['w', 'a', 's', 'd', '1', '2', '3', '4', '5', 'p', 'o', 'b', 'n', 'm', 'v', 'x', 'l']:
        print(f'alphanumeric key {key.char} pressed')
        commands = {
            'w': 'motor:forward',
            'a': 'motor:left',
            's': 'motor:backward',
            'd': 'motor:right',
            '1': 'motor:speed:50',
            '2': 'motor:speed:100',
            '3': 'motor:speed:150',
            '4': 'motor:speed:200',
            '5': 'motor:speed:255',
            'p': 'servo:armheight:150',
            'o': 'servo:armheight:90',
            'b': 'lights:animation:blink_left',
            'n': 'lights:animation:blink_right',
            'm': 'lights:animation:police',
            'v': 'lights:animation:blink_all',
            'x': 'lights:animation:off',
            'l': toggle_lights
        }
        command = commands.get(key.char)
        if callable(command):
            command()
        elif command:
            ser.write(f'{command}\n'.encode())

def toggle_lights():
    global is_light_on
    if is_light_on:
        ser.write('lights:front:0:0:0\n'.encode())
        ser.write('lights:back:0:0:0\n'.encode())
    else:
        ser.write('lights:front:255:255:255\n'.encode())
        ser.write('lights:back:255:255:0\n'.encode())
    is_light_on = not is_light_on

def handle_arrow_key(key):
    global camera_yaw, camera_pitch
    if key == keyboard.Key.left:
        camera_yaw = np.clip(camera_yaw + 10, 0, 180)
    elif key == keyboard.Key.right:
        camera_yaw = np.clip(camera_yaw - 10, 0, 180)
    elif key == keyboard.Key.down:
        camera_pitch = np.clip(camera_pitch + 10, 0, 180)
    elif key == keyboard.Key.up:
        camera_pitch = np.clip(camera_pitch - 10, 0, 180)
    ser.write(f'servo:cam_yaw:{camera_yaw}\n'.encode())
    ser.write(f'servo:cam_pitch:{camera_pitch}\n'.encode())

def on_release(key):
    ser.write('motor:stop\n'.encode())
    print(f'{key} released')
    if key == keyboard.Key.esc:
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
    global battery_voltage, humidity, temperature

    ser.flushInput()  # Clear the input buffer
    ser.write('read:battery\n'.encode())
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode().strip()
            if "Battery Voltage:" in line:
                battery_voltage = line.split(":")[1].strip()
                break
    ser.write('read:dht\n'.encode())
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

def opencv_code():
    global battery_voltage, humidity, temperature, camera_yaw
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    sleep(0.1)
    counter = 0
    for still in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True, resize=camera.resolution):
        image = still.array
        height, width = image.shape[:2]
        counter += 1
        if counter > 100:
            counter = 0
            read_serial_data()
        cv.putText(image, f'Battery: {battery_voltage}V', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.putText(image, f'Humidity: {humidity}%', (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.putText(image, f'Temp: {temperature}C', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        fov_center = (width - 100, height - 100)
        draw_camera_fov(image, camera_yaw, fov_center)
        cv.imshow("Display", image)
        rawCapture.truncate(0)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break
    camera.close()

def robot_drive_code():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def lidar_code():
    lidar = PyRPlidar()
    sleep(2)
    cv.namedWindow("RPLidar", cv.WINDOW_NORMAL)
    cv.resizeWindow("RPLidar", 400, 400)
    frame = 255 * np.zeros((400, 400, 3), dtype=np.uint8)
    while True:
        lidar.connect(port="/dev/ttyUSB1", baudrate=115200, timeout=3)
        lidar.set_motor_pwm(500)
        print(lidar.get_health(), lidar.get_info(), lidar.get_samplerate())
        scan_generator = lidar.start_scan_express(4)
        sleep(0.5)
        for count, scan in enumerate(scan_generator()):
            x = int(scan.distance * np.cos(np.radians(scan.angle)))
            y = int(scan.distance * np.sin(np.radians(scan.angle)))
            cv.circle(frame, (int(x/10) + 200, int(y/10) + 200), 2, (0, 255, 0), -1)
            if count % 10 == 0:
                cv.imshow("RPLidar", frame)
                cv.waitKey(1)
            if count > 4000:
                frame = 255 * np.zeros((400, 400, 3), dtype=np.uint8)
                break
        lidar.stop()
        lidar.disconnect()
        sleep(2)

if __name__ == "__main__":
    thread_robot_control = threading.Thread(target=robot_drive_code)
    thread_opencv = threading.Thread(target=opencv_code)
    thread_lidar = threading.Thread(target=lidar_code)
    thread_lidar.start()
    thread_opencv.start()
    thread_robot_control.start()
