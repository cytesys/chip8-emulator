import random

class Chip(object):
    """The CHIP8 interpreter"""
    def __init__(self, mem):
        """Initialization of the Chip object"""
        # Registers V0 to VF
        # VF is also the flags register
        self.V = [0] * 16

        # 16-bit register for memory addresses
        self.I = 0

        # The stack and stack pointer
        self.stack = [0] * 48
        self.SP = 0

        # The program counter
        self.PC = 0x200

        # Reference to the Memory object
        self.mem = mem

        # Screen
        self.screen = [0] * (64 * 32)
        self.screen_needs_update = True

        # Timers
        self.delay_timer = 0
        self.sound_timer = 0 # Sound timer is implemented, but not used properly (aka no sound)

        # Input
        self.key = [0] * 16

    def step(self):
        """Execute one instruction"""
        # Fetch the opcode
        opcode = (self.mem.read(self.PC) << 8) | self.mem.read(self.PC+1)

        # For debugging purposes
        #print(f"Opcode: {hex(opcode)} @ Address: {hex(self.PC)}")

        # Decode the opcode
        if opcode == 0x00e0:
            # 0x00E0
            # Clear screen
            for i in range(64 * 32):
                self.screen[i] = 0

            self.screen_needs_update = True

            self.PC += 2

        elif opcode == 0x00ee:
            # 0x00EE
            # Return from subroutine
            self.PC = ((self.stack[self.SP - 2] << 8) | self.stack[self.SP - 1]) + 2
            self.SP -= 2

        elif (opcode & 0xf000) == 0x0000:
            # 0x0NNN
            # Call user program
            self.PC = (opcode & 0x0fff)

        elif (opcode & 0xf000) == 0x1000:
            # 0x1NNN
            # Goto NNN
            self.PC = (opcode & 0x0fff)

        elif (opcode & 0xf000) == 0x2000:
            # 0x2NNN
            # Call subroutine at NNN
            self.stack[self.SP] = (self.PC & 0xff00) >> 8
            self.stack[self.SP + 1] = self.PC & 0x00ff
            self.SP += 2
            self.PC = opcode & 0x0fff

        elif (opcode & 0xf000) == 0x3000:
            # 0x3XNN
            # Skip next instruction if VX == NN
            x = (opcode & 0xf00) >> 8
            nn = opcode & 0xff
            
            if self.V[x] == nn:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xf000) == 0x4000:
            # 0x4XNN
            # Skip next instruction if VX != NN
            x = (opcode & 0xf00) >> 8
            nn = opcode & 0xff
            
            if self.V[x] != nn:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xf000) == 0x5000:
            # 0x5XY0
            # Skip next instruction if VX == VY
            x = (opcode & 0x0f00) >> 8
            y = (opcode & 0x00f0) >> 4
            
            if self.V[x] == self.V[y]:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xf000) == 0x6000:
            # 0x6XNN
            # Sets VX to NN
            x = (opcode & 0x0f00) >> 8
            nn = opcode & 0x00ff

            self.V[x] = nn
            self.PC += 2

        elif (opcode & 0xf000) == 0x7000:
            # 0x7XNN
            # Adds VX to NN
            x = (opcode & 0x0f00) >> 8
            nn = opcode & 0x00ff

            self.V[x] = (self.V[x] + nn) % 256
            self.PC += 2

        elif (opcode & 0xf000) == 0x8000:
            if (opcode & 0xf) == 0:
                # 0x8XY0
                # Sets VX to the value of VY
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                self.V[x] = self.V[y]
                self.PC += 2

            elif (opcode & 0xf) == 1:
                # 0x8XY1
                # Sets VX to VX or VY
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                self.V[x] |= self.V[y]
                self.PC += 2

            elif (opcode & 0xf) == 2:
                # 0x8XY2
                # Sets VX to VX & VY
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                self.V[x] &= self.V[y]
                self.PC += 2

            elif (opcode & 0xf) == 3:
                # 0x8XY3
                # Sets VX to VX ^ VY
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                self.V[x] ^= self.V[y]
                self.PC += 2

            elif (opcode & 0xf) == 4:
                # 0x8XY4
                # Adds VY to VX
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                sum = self.V[x] + self.V[y]
                if sum >= 256:
                    # Carry
                    self.V[0xf] = 1
                else:
                    self.V[0xf] = 0

                self.V[x] = sum % 256
                self.PC += 2

            elif (opcode & 0xf) == 5:
                # 0x8XY5
                # Subtracts VY from VX
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                sum = self.V[x] - self.V[y]
                if sum < 0:
                    # Borrow
                    self.V[0xf] = 1
                    sum += 256
                else:
                    self.V[0xf] = 0

                self.V[x] = sum
                self.PC += 2

            elif (opcode & 0xf) == 6:
                # 0x8XY6
                # Right shift VX by 1 and store LSB in VF
                x = (opcode & 0x0f00) >> 8

                self.V[0xf] = self.V[x] & 0x1

                self.V[x] >>= 1
                self.PC += 2

            elif (opcode & 0xf) == 7:
                # 0x8XY7
                # Set VX to VY - VX
                x = (opcode & 0x0f00) >> 8
                y = (opcode & 0x00f0) >> 4

                sum = self.V[y] - self.V[x]
                if sum < 0:
                    # Borrow
                    self.V[0xf] = 1
                    sum += 256
                else:
                    self.V[0xf] = 0

                self.V[x] = sum
                self.PC += 2

            elif (opcode & 0xf) == 0xe:
                # 0x8XYE
                # Left shift VX by 1 and store MSB in VF
                x = (opcode & 0x0f00) >> 8

                self.V[0xf] = (self.V[x] & 0x80) >> 7

                self.V[x] = (self.V[x] << 1) % 256
                self.PC += 2

            else:
                raise Exception(f"The opcode {hex(opcode)} is not implemented!")
        
        elif (opcode & 0xf000) == 0x9000:
            # 0x9XY0
            # Skip if VX != VY
            x = (opcode & 0x0f00) >> 8
            y = (opcode & 0x00f0) >> 4
            
            if self.V[x] != self.V[y]:
                self.PC += 4
            else:
                self.PC += 2

        elif (opcode & 0xf000) == 0xa000:
            # 0xANNN
            # Sets I to the address NNN
            self.I = opcode & 0x0fff
            self.PC += 2

        elif (opcode & 0xf000) == 0xb000:
            # 0xBNNN
            # Sets PC to V0 + NNN
            self.PC = self.V[0] + (opcode & 0x0fff)

        elif (opcode & 0xf000) == 0xc000:
            # 0xCXNN
            # Sets VX to <random> & NN
            x = (opcode & 0x0f00) >> 8
            nn = opcode & 0x00ff
            rand = random.randint(0, 255)

            self.V[x] = rand & nn
            self.PC += 2

        elif (opcode & 0xf000) == 0xd000:
            # 0xDXYN
            # Draw sprite at (VX, VY).
            # N is the height of the sprite.
            # Sprite is read from address I.
            x = (opcode & 0x0f00) >> 8
            y = (opcode & 0x00f0) >> 4
            n = opcode & 0x000f

            for i in range(n):
                index = ((self.V[y] + i) * 64) + self.V[x]
                row = self.mem.read(self.I + i)

                for j in range(8):
                    if (index + j) >= len(self.screen):
                        break

                    oldpixel = self.screen[(index + j)]
                    newpixel = (row >> (7 - j)) & 0x1

                    self.screen[(index + j)] = oldpixel ^ newpixel

                    if (oldpixel == 1 and newpixel == 1):
                        # Collision
                        self.V[0xf] = 1

            self.screen_needs_update = True
            self.PC += 2

        elif (opcode & 0xf000) == 0xe000:
            if (opcode & 0x00ff) == 0x9e:
                # 0xEX9E
                # Skip next instruction if key in VX is pressed
                x = (opcode & 0x0f00) >> 8
                
                assert self.V[x] < 16
                if self.key[self.V[x]] == 1:
                    self.PC += 4
                else:
                    self.PC += 2

            elif (opcode & 0x00ff) == 0xa1:
                # 0xEXA1
                # Skip next instruction if key in VX is not pressed
                x = (opcode & 0x0f00) >> 8

                assert self.V[x] < 16
                if self.key[self.V[x]] == 0:
                    self.PC += 4
                else:
                    self.PC += 2
            
            else:
                raise Exception(f"The opcode {hex(opcode)} is not implemented!")

        elif (opcode & 0xf000) == 0xf000:
            if (opcode & 0x00ff) == 0x07:
                # 0xFX07
                # Set VX to value of the delay timer
                x = (opcode & 0x0f00) >> 8

                self.V[x] = self.delay_timer
                self.PC += 2

            elif (opcode & 0x00ff) == 0x0a:
                # 0xFX0A
                # Wait for keypress and store key in VX
                x = (opcode & 0x0f00) >> 8

                # Scan every key
                for i in range(16):
                    if self.key[i] == 1:
                        # Key is found
                        # Move on in the program
                        self.V[x] = i
                        self.PC += 2
                        break

                # Reexecute the instruction at the next cycle

            elif (opcode & 0x00ff) == 0x15:
                # 0xFX15
                # Set delay timer to VX
                x = (opcode & 0x0f00) >> 8

                self.delay_timer = self.V[x]

                self.PC += 2

            elif (opcode & 0x00ff) == 0x18:
                # 0xFX18
                # Set sound timer to VX
                x = (opcode & 0x0f00) >> 8

                self.sound_timer = self.V[x]

                self.PC += 2

            elif (opcode & 0x00ff) == 0x1e:
                # 0xFX1E
                # Adds VX to I
                x = (opcode & 0x0f00) >> 8

                self.I += self.V[x]

                self.PC += 2
            
            elif (opcode & 0x00ff) == 0x29:
                # 0xFX29
                # Sets I to the address of character in VX
                x = (opcode & 0x0f00) >> 8

                self.I = self.V[x] * 5

                self.PC += 2

            elif (opcode & 0x00ff) == 0x33:
                # 0xFX33
                # Store BCD of VX
                x = (opcode & 0x0f00) >> 8

                self.mem.write(self.I, self.V[x] // 100)
                self.mem.write(self.I + 1, (self.V[x] // 10) % 10)
                self.mem.write(self.I + 2, self.V[x] % 10)

                self.PC += 2

            elif (opcode & 0x00ff) == 0x55:
                # 0xFX55
                # Store V0 to VX in memory at address I
                x = (opcode & 0x0f00) >> 8

                for i in range(x + 1):
                    self.mem.write(self.I + i, self.V[i])

                self.PC += 2

            elif (opcode & 0x00ff) == 0x65:
                # 0xFX65
                # Fills V0 to VX from memory at address I
                x = (opcode & 0x0f00) >> 8

                for i in range(x + 1):
                    self.V[i] = self.mem.read(self.I + i)

                self.PC += 2

        else:
            raise Exception(f"The opcode {hex(opcode)} is not implemented!")

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 10
            if self.delay_timer < 0:
                self.delay_timer = 0

        if self.sound_timer > 0:
            self.sound_timer -= 10
            if self.sound_timer < 0:
                self.sound_timer = 0
