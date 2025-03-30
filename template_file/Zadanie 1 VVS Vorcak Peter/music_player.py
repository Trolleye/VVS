import time
import _thread
from music.play import *
from machine import Pin


class MusicPlayer:
    def __init__(self):
        self.pin_button = Pin(2, Pin.IN, Pin.PULL_UP)
        if hasattr(_thread, "start_new_thread"): # vyhadzovalo warning Cannot find reference 'start_new_thread' in '_thread.pyi'
            _thread.start_new_thread(self.check_button, ())

    def check_button(self):
        while True:
            if self.pin_button.value() == 0:
                self.change_volume()
                time.sleep(0.5)

    def prompt_user(self):
        while True:
            print("1. Happy Birthday - 7")
            print("2. At Doom's Gate - 19")
            print("3. Pacman - 2")
            print("4. Take on Me - 34")
            print("5. The Godfather Theme - 39")

            choice = input("Choose a song from 1 - 5: ")

            try:
                choice = int(choice)
                if 1 <= choice <= 5:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        song_map = {1: 7, 2: 19, 3: 2, 4: 34, 5: 39}
        user_song = song_map.get(choice)
        self.play_song(user_song)

    @staticmethod
    def change_volume():
        while True:
            try:
                user_volume = int(input("Enter volume (0-32768): "))
                if 0 <= user_volume <= 32768:
                    set_volume(user_volume)
                else:
                    print("Invalid input. Please enter a number between 0 and 32768.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def play_song(song):
        set_volume(100)
        print(f"Playing song {song}...")
        playsong(melody[int(song)])

