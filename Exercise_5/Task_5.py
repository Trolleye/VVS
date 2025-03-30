from machine import Pin
import time

class ButtonController:
    def __init__(self):
        self.pin_button = Pin(2, Pin.IN, Pin.PULL_UP)
        self.button_presses = 0
        self.monitor_button()

    def monitor_button(self):
        previous_state = 1
        while True:
            current_state = self.pin_button.value()
            if previous_state == 1 and current_state == 0:
                print(self.get_button_state())
            previous_state = current_state
            time.sleep(0.01)

    def press_button(self):
        self.button_presses += 1
        print("Button Pressed " + str(self.button_presses) + " times")

    def get_button_state(self):
        if self.pin_button.value() == 1:
            return False
        if self.pin_button.value() == 0:
            return True


controller = ButtonController()