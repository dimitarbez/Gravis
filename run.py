import RPi.GPIO as GPIO
import curses
from motor_controller import MotorController

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

fl_motor_pwm_pin = 23
fl_motor_in1 = 29
fl_motor_in2 = 31
fr_motor_in3 = 33
fr_motor_in4 = 35
fr_motor_pwm_pin = 37

bl_motor_pwm_pin = 24
bl_motor_in1 = 26
bl_motor_in2 = 32
br_motor_in3 = 36
br_motor_in4 = 38
br_motor_pwm_pin = 40


if __name__ == '__main__':

    try:

        print('program started')

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(fl_motor_pwm_pin, GPIO.OUT)
        GPIO.setup(fr_motor_pwm_pin, GPIO.OUT)
        GPIO.setup(fl_motor_in1, GPIO.OUT)
        GPIO.setup(fl_motor_in2, GPIO.OUT)
        GPIO.setup(fr_motor_in3, GPIO.OUT)
        GPIO.setup(fr_motor_in4, GPIO.OUT)
        GPIO.setup(bl_motor_pwm_pin, GPIO.OUT)
        GPIO.setup(br_motor_pwm_pin, GPIO.OUT)
        GPIO.setup(bl_motor_in1, GPIO.OUT)
        GPIO.setup(bl_motor_in2, GPIO.OUT)
        GPIO.setup(br_motor_in3, GPIO.OUT)
        GPIO.setup(br_motor_in4, GPIO.OUT)

        motorcontroller = MotorController()

        while True:
            char = screen.getch()

            print(char)

            if char == ord('q'):
                motorcontroller.stop()
                break
            elif char == ord('w'):
                motorcontroller.moveforward()
            elif char == ord('s'):
                motorcontroller.movebackward()
            elif char == ord('a'):
                motorcontroller.moveleft()
            elif char == ord('d'):
                motorcontroller.moveright()
            elif char == ord('e'):
                motorcontroller.stop()
            elif char == ord('z'):
                motorcontroller.movehardleft()
            elif char == ord('c'):
                motorcontroller.movehardright()
            elif char == ord('1'):
                motorcontroller.setmotorspeed(20)
            elif char == ord('2'):
                motorcontroller.setmotorspeed(40)
            elif char == ord('3'):
                motorcontroller.setmotorspeed(60)
            elif char == ord('4'):
                motorcontroller.setmotorspeed(80)
            elif char == ord('5'):
                motorcontroller.setmotorspeed(100)
            elif char == ord(','):
                motorcontroller.offsetmotorspeed(-5)
            elif char == ord('.'):
                motorcontroller.offsetmotorspeed(+5)

    except Exception as err:
        print(err.args[0])

    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
