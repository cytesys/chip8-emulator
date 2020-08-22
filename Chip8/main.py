import tkinter as tk
from modules.Chip import Chip
from modules.Memory import Memory

class App(object):
    """
    Main widget, containing the GUI, Memory and Chip.
    """
    def __init__(self, master):
        """
        Initialization of the main widget.
        """
        # Create GUI
        self.canvas = tk.Canvas(master, width=640, height=320, bg="#000000")
        master.bind("<KeyPress>", self.register_keydown)
        master.bind("<KeyRelease>", self.register_keyup)
        self.canvas.pack()

        # Create new Memory object, and load a file
        self.mem = Memory()
        self.mem.load("../roms/Maze.ch8")

        # Createnew Chip object
        self.chip = Chip(self.mem)

        # Start the main loop of this widget
        self.canvas.after(10, func=self.run)

    def run(self):
        """
        The main loop of this widget.
        """
        # Step one instruction
        self.chip.step()

        # Redraw screen if necessary
        if self.chip.screen_needs_update:
            self.canvas.delete(tk.ALL)
            for y in range(32):
                for x in range(64):
                    if self.chip.screen[y * 64 + x] > 0:
                        self.canvas.create_rectangle(x * 10, y * 10, (x * 10) + 10, (y * 10) + 10, fill="white")
                    else:
                        self.canvas.create_rectangle(x * 10, y * 10, (x * 10) + 10, (y * 10) + 10, fill="black")
            self.chip.screen_needs_update = False
        
        # Trigger a new run cycle
        self.canvas.after(1, func=self.run)

    def register_keydown(self, event):
        """
        Handler for keypresses.
        """
        # Set the appropriate key for the Chip object
        if event.char == '1':
            self.chip.key[1] = 1
        elif event.char == '2':
            self.chip.key[2] = 1
        elif event.char == '3':
            self.chip.key[3] = 1
        elif event.char == '4':
            self.chip.key[0xc] = 1
        elif event.char == 'q':
            self.chip.key[4] = 1
        elif event.char == 'w':
            self.chip.key[5] = 1
        elif event.char == 'e':
            self.chip.key[6] = 1
        elif event.char == 'r':
            self.chip.key[0xd] = 1
        elif event.char == 'a':
            self.chip.key[7] = 1
        elif event.char == 's':
            self.chip.key[8] = 1
        elif event.char == 'd':
            self.chip.key[9] = 1
        elif event.char == 'f':
            self.chip.key[0xe] = 1
        elif event.char == 'z':
            self.chip.key[0xa] = 1
        elif event.char == 'x':
            self.chip.key[0] = 1
        elif event.char == 'c':
            self.chip.key[0xb] = 1
        elif event.char == 'v':
            self.chip.key[0xf] = 1

    def register_keyup(self, event):
        """
        Handler for key releases.
        """
        # Unset the appropriate key for the Chip object
        if event.char == '1':
            self.chip.key[1] = 0
        elif event.char == '2':
            self.chip.key[2] = 0
        elif event.char == '3':
            self.chip.key[3] = 0
        elif event.char == '4':
            self.chip.key[0xc] = 0
        elif event.char == 'q':
            self.chip.key[4] = 0
        elif event.char == 'w':
            self.chip.key[5] = 0
        elif event.char == 'e':
            self.chip.key[6] = 0
        elif event.char == 'r':
            self.chip.key[0xd] = 0
        elif event.char == 'a':
            self.chip.key[7] = 0
        elif event.char == 's':
            self.chip.key[8] = 0
        elif event.char == 'd':
            self.chip.key[9] = 0
        elif event.char == 'f':
            self.chip.key[0xe] = 0
        elif event.char == 'z':
            self.chip.key[0xa] = 0
        elif event.char == 'x':
            self.chip.key[0] = 0
        elif event.char == 'c':
            self.chip.key[0xb] = 0
        elif event.char == 'v':
            self.chip.key[0xf] = 0

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
