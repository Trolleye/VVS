from machine import Pin, PWM
import time


class LEDController:
    def __init__(self):
        self.pin_blue = PWM(Pin(10), freq=120, duty_u16=0)
        self.pin_green = PWM(Pin(11), freq=120, duty_u16=0)
        self.pin_red = PWM(Pin(21), freq=120, duty_u16=0)
        self.pin_boot = Pin(9, Pin.IN, Pin.PULL_UP)

    def reset_led(self):
        self.pin_red.duty_u16(0)
        self.pin_green.duty_u16(0)
        self.pin_blue.duty_u16(0)

    def led_green(self):
        self.reset_led()
        self.pin_green.duty_u16(1023*64)

    def led_red(self):
        self.reset_led()
        self.pin_red.duty_u16(1023*64)

    def led_blue(self):
        self.reset_led()
        self.pin_blue.duty_u16(1023*64)

    def led_turquoise(self):
        self.reset_led()
        self.pin_green.duty_u16(1023*64)
        self.pin_blue.duty_u16(1023*64)

    def led_pink(self):
        self.reset_led()
        self.pin_red.duty_u16(1023*64)
        self.pin_blue.duty_u16(1023*64)

    def led_yellow(self):
        self.reset_led()
        self.pin_green.duty_u16(1023*64)
        self.pin_red.duty_u16(1023*64)

    def led_white(self):
        self.reset_led()
        self.pin_green.duty_u16(1023*64)
        self.pin_red.duty_u16(1023*64)
        self.pin_blue.duty_u16(1023*64)

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



    def read_pwm(self):
        previous_state = 1
        self.prompt_led_colors()
        buzzer = BuzzerController()
        buzzer_duty = buzzer.read_buzzer_percent()
        buzzer_freq = buzzer.read_buzzer_frequency()
        buzzer.pin_buzzer.duty_u16(int(buzzer_duty))
        buzzer.pin_buzzer.freq(buzzer_freq)
        while True:
            current_state = self.pin_boot.value()
            if previous_state == 1 and current_state == 0:
                self.prompt_led_colors()
            previous_state = current_state
            time.sleep(0.01)

    @staticmethod
    def read_rgb_pwm(color):
        while True:
            try:
                value = int(input(f"Enter duty cycle value for {color} (0-1023): "))
                if 0 <= value <= 1023:
                    return value * 64
                else:
                    print("Value must be in range 0-1023. Please try again.")
            except ValueError:
                print("Please enter a valid integer.")


    def prompt_led_colors(self):
        self.reset_led()
        red_duty = self.read_rgb_pwm("red")
        green_duty = self.read_rgb_pwm("green")
        blue_duty = self.read_rgb_pwm("blue")
        self.pin_red.duty_u16(red_duty)
        self.pin_green.duty_u16(green_duty)
        self.pin_blue.duty_u16(blue_duty)

    def pwm_cycle(self):
        self.prompt_led_colors()
        previous_state = 1
        while True:
            current_state = self.pin_boot.value()
            if previous_state == 1 and current_state == 0:
                self.prompt_led_colors()
            previous_state = current_state
            time.sleep(0.01)


    def smooth_transition(self, start_duties, end_duties, duration):
        steps = 100
        delay = duration / (3 * steps)
        for i in range(steps + 1):
            self.pin_red.duty_u16(int(start_duties[0] + (end_duties[0] - start_duties[0]) * i / steps))
            self.pin_green.duty_u16(int(start_duties[1] + (end_duties[1] - start_duties[1]) * i / steps))
            self.pin_blue.duty_u16(int(start_duties[2] + (end_duties[2] - start_duties[2]) * i / steps))
            time.sleep(delay)

    def led_timed_cycle(self):
        while True:
            try:
                cycle_time = int(input("Enter cycle time (1-5 seconds): "))
                if 1 <= cycle_time <= 5:
                    break
                print("Time must be between 1-5 seconds.")
            except ValueError:
                print("Please enter a valid integer.")

        rgb_colors = [
            (1023, 0, 0),   # Red
            (0, 1023, 0),   # Green
            (0, 0, 1023)    # Blue
        ]

        while True:
            for i in range(len(rgb_colors)):
                start_duties = rgb_colors[i]
                end_duties = rgb_colors[(i + 1) % len(rgb_colors)]
                self.smooth_transition(start_duties, end_duties, cycle_time)


class BuzzerController:
    def __init__(self):
        self.pin_buzzer = PWM(Pin(5), freq=20, duty_u16=0)

    @staticmethod
    def read_buzzer_duty_cycle():
        while True:
            try:
                duty = int(input("Enter duty cycle value for buzzer (0-1023): "))
                if 0 <= duty <= 1023:
                    return duty * 64
                print("Duty cycle must be between 0-1023")
            except ValueError:
                print("Please enter a valid integer")

    @staticmethod
    def read_buzzer_frequency():
        while True:
            try:
                freq = int(input("Enter frequency for buzzer (20-20000): "))
                if 20 <= freq <= 20000:
                    return freq
                print("Frequency must be between 20-20000")
            except ValueError:
                print("Please enter a valid integer")

    @staticmethod
    def read_buzzer_percent():
        while True:
            try:
                duty = int(input("Enter duty cycle percentage for buzzer (0%-100%): "))
                if 0 <= duty <= 100:
                    duty16 = duty * 654.72 / 2
                    return duty16
                print("Percentage must be between 0% and 100%")
            except ValueError:
                print("Please enter a valid integer")

controller = LEDController()