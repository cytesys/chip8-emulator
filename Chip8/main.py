import tkinter as tk
import argparse
import os
from modules import Chip
from modules import Memory
from modules import Keyboard

class App(object):
    """Main widget, containing the GUI, Memory and Chip."""
    def __init__(self, master, file):
        """Initialization of the main widget."""
        self.screen_width = 64
        self.screen_height = 32

        # Create GUI
        self.canvas = tk.Canvas(
            master,
            width=self.screen_width * 10,
            height=self.screen_height * 10,
            bg="#000000"
        )
        master.bind("<KeyPress>", self.register_keydown)
        master.bind("<KeyRelease>", self.register_keyup)
        self.canvas.pack()

        # Create new Memory object, and load a file
        self.mem = Memory()

        try:
            self.mem.load(file)
        except FileNotFoundError:
            print("The file does not exist!")
            exit(1)

        # Create new Chip object
        self.chip = Chip(self.mem)

        # Create a keyboard handler
        self.keyboard = Keyboard(self.chip)

        # Start the main loop of this widget
        self.canvas.after(10, func=self.run)

    def run(self):
        """The main loop of this widget."""
        # Step one instruction
        self.chip.step()

        # Redraw screen if necessary
        if self.chip.screen_needs_update:
            self.canvas.delete(tk.ALL)
            for y in range(self.screen_height):
                for x in range(self.screen_width):
                    if self.chip.screen[y * self.screen_width + x] > 0:
                        self.canvas.create_rectangle(
                            x * 10,
                            y * 10,
                            (x * 10) + 10,
                            (y * 10) + 10,
                            fill="white"
                        )

            self.chip.screen_needs_update = False
        
        # Trigger a new run cycle
        self.canvas.after(1, func=self.run)

    def register_keydown(self, event):
        """Handler for keypresses."""
        self.keyboard.set(event.char)

    def register_keyup(self, event):
        """Handler for key releases."""
        self.keyboard.unset(event.char)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chip8 emulator')
    parser.add_argument('file')
    args = parser.parse_args()
    file = os.path.abspath(args.file)

    root = tk.Tk()
    app = App(root, file)
    root.mainloop()
