import curses
from motor_controller import MotorController

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)    

if __name__ == '__main__':

    try:

        motorcontroller = MotorController()
        
        while True:
            char = screen.getch()
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

    finally:
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()