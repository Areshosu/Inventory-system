import os
import sys
import subprocess
import time
import inspect

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def restart_console():
    subprocess.call([sys.executable] + sys.argv)

def showMessageAndRestart(message: str):
    clear_console()
    countdown = 3

    while countdown != 0:
        print(f"{message} ({countdown})", end='\r')
        countdown -= 1
        time.sleep(1)

    clear_console()
    restart_console()

def showMessageAndRedirectToMainPage(self, message: str):
    clear_console()
    countdown = 3

    while countdown != 0:
        print(f"{message} ({countdown})", end='\r')
        countdown -= 1
        time.sleep(1)

    self.menuPage()

def getCallerName():
    frame = inspect.currentframe().f_back
    return frame.f_code.co_name

def logToFile(message: str):
    file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Storage", "logging.txt"), mode="w")
    file.write(message)
    file.close()