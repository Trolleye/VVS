from machine import Pin, PWM
import time


class LEDController:
    def __init__(self):
        self.pin_blue = PWM(Pin(10), freq=120, duty_u16=0)
        self.pin_green = PWM(Pin(11), freq=120, duty_u16=0)
        self.pin_red = PWM(Pin(21), freq=120, duty_u16=0)
        self.pin_buzzer = PWM(Pin(13), freq=1, duty_u16=0)
        self.pin_boot = Pin(9, Pin.IN, Pin.PULL_UP)
        self.pwm_cycle()


    def reset_led(self):
        self.pin_red.duty_u16(0)
        self.pin_green.duty_u16(0)
        self.pin_blue.duty_u16(0)

    def led_green(self):
        self.reset_led()
        self.pin_green.duty_u16(self.read_rgb_pwm("green"))

    def led_red(self):
        self.reset_led()
        self.pin_red.duty_u16(self.read_rgb_pwm("red"))

    def led_blue(self):
        self.reset_led()
        self.pin_blue.duty_u16(self.read_rgb_pwm("blue"))

    def led_turquoise(self):
        self.reset_led()
        duty = self.read_rgb_pwm("turquoise")
        self.pin_green.duty_u16(duty)
        self.pin_blue.duty_u16(duty)

    def led_pink(self):
        self.reset_led()
        duty = self.read_rgb_pwm("pink")
        self.pin_red.duty_u16(duty)
        self.pin_blue.duty_u16(duty)

    def led_yellow(self):
        self.reset_led()
        duty = self.read_rgb_pwm("yellow")
        self.pin_green.duty_u16(duty)
        self.pin_red.duty_u16(duty)

    def led_white(self):
        self.reset_led()
        duty = self.read_rgb_pwm("white")
        self.pin_green.duty_u16(duty)
        self.pin_red.duty_u16(duty)
        self.pin_blue.duty_u16(duty)

    def led_black(self):
        self.reset_led()

    def set_led(self, light_number):
        if light_number == 1:
            self.led_red()
        elif light_number == 2:
            self.led_green()
        elif light_number == 3:
            self.led_blue()
        elif light_number == 4:
            self.led_turquoise()
        elif light_number == 5:
            self.led_pink()
        elif light_number == 6:
            self.led_yellow()
        elif light_number == 7:
            self.led_white()
        elif light_number == 8:
            self.led_black()

    def cycle_colors(self):
        while True:
            self.led_blue()
            time.sleep(1)
            self.led_pink()
            time.sleep(0.8)
            self.led_green()
            time.sleep(2)
            self.led_yellow()
            time.sleep(1.5)
            self.led_red()
            time.sleep(1.2)
            self.led_turquoise()
            time.sleep(0.9)
            self.led_white()
            time.sleep(3)

    def prompt_user(self):
        self.reset_led()
        is_color_range = False
        is_time_range = False
        led_color_number = 0
        led_sleep_time = 0
        while not is_color_range:
            try:
                user_color_input = int(input("Choose a number 1 - 8: "))
                if 1 <= user_color_input <= 8:
                    is_color_range = True
                    led_color_number = user_color_input
                else:
                    print("Number out of range.")
            except ValueError:
                print("Not a number...")

        while not is_time_range:
            try:
                user_time_input = int(input("Choose a time 1 - 10 in seconds: "))
                if 1 <= user_time_input <= 10:
                    led_sleep_time = user_time_input
                    is_time_range = True
                else:
                    print("Number out of range.")
            except ValueError:
                print("Not a number...")

        self.set_led(led_color_number)
        time.sleep(led_sleep_time)
        self.set_led(8)

    @staticmethod
    def read_buzzer_pwm():
        while True:  # Keep asking until valid input
            try:
                duty = int(input("Enter duty cycle value for buzzer (0-1023): "))
                if not 0 <= duty <= 1023:
                    print("Duty cycle must be between 0-1023")
                    continue  # Skip to next iteration

                freq = int(input("Enter frequency for buzzer (20-20000): "))
                if not 20 <= freq <= 20000:
                    print("Frequency must be between 20-20000")
                    continue  # Skip to next iteration

                return duty, freq  # Only return when both values are valid

            except ValueError:
                print("Please enter valid integers")

    @staticmethod
    def read_rgb_pwm(color):
        while True:
            try:
                value = int(input(f"Enter duty cycle value for {color} (0-1023): "))
                if 0 <= value <= 1023:
                    return value * 64 #64 kedze robim v pycharme a pouzivam duty16
                else:
                    print("Value must be in range 0-1023. Please try again.")
            except ValueError:
                print("Please enter a valid integer.")


    def prompt_user_pwm(self):
        self.reset_led()
        red_duty = self.read_rgb_pwm("red")
        green_duty = self.read_rgb_pwm("green")
        blue_duty = self.read_rgb_pwm("blue")
        self.pin_red.duty_u16(red_duty)
        self.pin_green.duty_u16(green_duty)
        self.pin_blue.duty_u16(blue_duty)

    def pwm_cycle(self):
        self.prompt_user_pwm()
        previous_state = 1
        while True:
            current_state = self.pin_boot.value()
            if previous_state == 1 and current_state == 0:
                self.prompt_user_pwm()
            previous_state = current_state
            time.sleep(0.01)



controller = LEDController()