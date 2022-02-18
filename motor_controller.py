import RPi.GPIO as GPIO


fl_motor_pwm_pin = 23
fl_motor_in1 = 29
fl_motor_in2 = 31
fr_motor_in3 = 33
fr_motor_in4 = 35
fr_motor_pwm_pin = 37

bl_motor_pwm_pin = 22
bl_motor_in1 = 26
bl_motor_in2 = 32
br_motor_in3 = 36
br_motor_in4 = 38
br_motor_pwm_pin = 40


class MotorController:

    def __init__(self):
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
        self.pwm_fl_motor = GPIO.PWM(fl_motor_pwm_pin, 200)
        self.pwm_fr_motor = GPIO.PWM(fr_motor_pwm_pin, 200)
        self.pwm_bl_motor = GPIO.PWM(bl_motor_pwm_pin, 200)
        self.pwm_br_motor = GPIO.PWM(br_motor_pwm_pin, 200)
        self.motorspeed = 50
        self.pwm_fl_motor.start(self.motorspeed)
        self.pwm_fr_motor.start(self.motorspeed)
        self.pwm_bl_motor.start(self.motorspeed)
        self.pwm_br_motor.start(self.motorspeed)
        self.stop()


    def offsetmotorspeed(self, speedoffset):
        if speedoffset > 0:
            if self.motorspeed < 100:
                self.motorspeed = self.motorspeed + speedoffset
        elif speedoffset < 0:
            if self.motorspeed > 0:
                self.motorspeed = self.motorspeed + speedoffset
        self.pwm_fl_motor.ChangeDutyCycle(self.motorspeed)
        self.pwm_fr_motor.ChangeDutyCycle(self.motorspeed)
        self.pwm_bl_motor.ChangeDutyCycle(self.motorspeed)
        self.pwm_br_motor.ChangeDutyCycle(self.motorspeed)


    def setmotorspeed(self, speed):
        self.motorspeed = speed
        self.pwm_fl_motor.ChangeDutyCycle(self.motorspeed)
        self.pwm_fr_motor.ChangeDutyCycle(self.motorspeed)
        self.pwm_bl_motor.ChangeDutyCycle(self.motorspeed)
        self.pwm_br_motor.ChangeDutyCycle(self.motorspeed)


    def moveforward(self):
        GPIO.output(fl_motor_in1, GPIO.LOW)
        GPIO.output(fl_motor_in2, GPIO.HIGH)
        GPIO.output(fr_motor_in3, GPIO.LOW)
        GPIO.output(fr_motor_in4, GPIO.HIGH)

        GPIO.output(bl_motor_in1, GPIO.LOW)
        GPIO.output(bl_motor_in2, GPIO.HIGH)
        GPIO.output(br_motor_in3, GPIO.LOW)
        GPIO.output(br_motor_in4, GPIO.HIGH)


    def movebackward(self):
        GPIO.output(fl_motor_in1, GPIO.HIGH)
        GPIO.output(fl_motor_in2, GPIO.LOW)
        GPIO.output(fr_motor_in3, GPIO.HIGH)
        GPIO.output(fr_motor_in4, GPIO.LOW)

        GPIO.output(bl_motor_in1, GPIO.HIGH)
        GPIO.output(bl_motor_in2, GPIO.LOW)
        GPIO.output(br_motor_in3, GPIO.HIGH)
        GPIO.output(br_motor_in4, GPIO.LOW)


    def moveright(self):
        GPIO.output(fl_motor_in1, GPIO.LOW)
        GPIO.output(fl_motor_in2, GPIO.LOW)
        GPIO.output(fr_motor_in3, GPIO.LOW)
        GPIO.output(fr_motor_in4, GPIO.HIGH)

        GPIO.output(bl_motor_in1, GPIO.LOW)
        GPIO.output(bl_motor_in2, GPIO.LOW)
        GPIO.output(br_motor_in3, GPIO.LOW)
        GPIO.output(br_motor_in4, GPIO.HIGH)


    def moveleft(self):
        GPIO.output(fl_motor_in1, GPIO.LOW)
        GPIO.output(fl_motor_in2, GPIO.HIGH)
        GPIO.output(fr_motor_in3, GPIO.LOW)
        GPIO.output(fr_motor_in4, GPIO.LOW)

        GPIO.output(bl_motor_in1, GPIO.LOW)
        GPIO.output(bl_motor_in2, GPIO.HIGH)
        GPIO.output(br_motor_in3, GPIO.LOW)
        GPIO.output(br_motor_in4, GPIO.LOW)


    def movehardright(self):
        GPIO.output(fl_motor_in1, GPIO.HIGH)
        GPIO.output(fl_motor_in2, GPIO.LOW)
        GPIO.output(fr_motor_in3, GPIO.LOW)
        GPIO.output(fr_motor_in4, GPIO.HIGH)

        GPIO.output(bl_motor_in1, GPIO.HIGH)
        GPIO.output(bl_motor_in2, GPIO.LOW)
        GPIO.output(br_motor_in3, GPIO.LOW)
        GPIO.output(br_motor_in4, GPIO.HIGH)


    def movehardleft(self):
        GPIO.output(fl_motor_in1, GPIO.LOW)
        GPIO.output(fl_motor_in2, GPIO.HIGH)
        GPIO.output(fr_motor_in3, GPIO.HIGH)
        GPIO.output(fr_motor_in4, GPIO.LOW)

        GPIO.output(bl_motor_in1, GPIO.LOW)
        GPIO.output(bl_motor_in2, GPIO.HIGH)
        GPIO.output(br_motor_in3, GPIO.HIGH)
        GPIO.output(br_motor_in4, GPIO.LOW)


    def stop(self):
        GPIO.output(fl_motor_in1, GPIO.LOW)
        GPIO.output(fl_motor_in2, GPIO.LOW)
        GPIO.output(fr_motor_in3, GPIO.LOW)
        GPIO.output(fr_motor_in4, GPIO.LOW)

        GPIO.output(bl_motor_in1, GPIO.LOW)
        GPIO.output(bl_motor_in2, GPIO.LOW)
        GPIO.output(br_motor_in3, GPIO.LOW)
        GPIO.output(br_motor_in4, GPIO.LOW)
