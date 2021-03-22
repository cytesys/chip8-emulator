class Memory(object):
    """The CHIP8 memory"""
    def __init__(self):
        """Initialize the memory."""
        # Initialize the memory
        self.mem = [0x0] * 0x1000

        # This is just pixel data for the font.
        self.mem[0x0 : 0x50] = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]

    def read(self, address):
        """
        Method to read from memory at the specified address. If the address is unaccessible,
        this method will throw an exception.
        """
        assert isinstance(address, int)

        if (address >= 0x000) and (address < 0xea0):
            # Used by the fontset and the user program.
            # Everything in between the fontset (0x50) and the user program (0x200) is
            # used in Super-CHIP programs, but we don't support that yet, so everything
            # there is empty.
            return self.mem[address]
        else:
            # 0xea0 - 0xeff were reserved for the call stack and variables and other stuff, so
            # it was not accessible directly from memory.
            # 0xf00 - 0xfff were reserved for display refresh, so it too was not directly accessed
            # from memory.
            # Because of this, these portions of the memory will throw an error if the program tries
            # to access it.
            raise Exception(f"Tried to read from non-accessable memory! mem@{hex(address)}")
    
    def write(self, address, byte):
        """
        Method to write data to memory.
        All of the user memory is writeable here, but I am unsure if
        that is actually correct...
        """
        assert isinstance(address, int)
        assert isinstance(byte, int)
        assert byte >= 0 and byte < 256

        if (address >= 0x200) and (address < 0xea0):
            # Used by the user program.
            self.mem[address] = byte
        else:
            raise Exception(f"Tried to write to non-accessable memory! mem@{hex(address)}")

    def load(self, file):
        """
        Method to load a user program into memory.
        """
        with open(file, 'rb') as file:
            index = 0x200
            byte = file.read(1)

            while byte:
                self.write(index, int.from_bytes(byte, byteorder="big", signed=False))
                index += 1
                byte = file.read(1)

            file.close()
