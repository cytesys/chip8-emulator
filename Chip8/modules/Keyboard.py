class Keyboard(object):
    """A class for mapping the CHIP8 keys to the computer keyboard"""
    def __init__(self, chip):
        """Initialization"""
        self.chip = chip

    def lookup(self, char):
        """A method to map keyboard keys to CHIP8 keys"""
        table = {
            '1': 0x1,
            '2': 0x2,
            '3': 0x3,
            '4': 0xc,
            'q': 0x4,
            'w': 0x5,
            'e': 0x6,
            'r': 0xd,
            'a': 0x7,
            's': 0x8,
            'd': 0x9,
            'f': 0xe,
            'z': 0xa,
            'x': 0x0,
            'c': 0xb,
            'v': 0xf
        }

        return table.get(char, -1)

    def set(self, char):
        """Method to set a CHIP8 key based on the keyboard input"""
        index = self.lookup(char)
        if not index == -1:
            self.chip.key[index] = 1;
    
    def unset(self, char):
        """Method to unset a CHIP8 key based on the keyboard input"""
        index = self.lookup(char)
        if not index == -1:
            self.chip.key[index] = 0;