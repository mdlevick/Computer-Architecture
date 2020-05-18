"""CPU functionality."""

import sys, inspect

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    #ram 00-FF
        self.reg = [0] * 8      #registers
        self.pc = 0             #program counter/current instruction
        self.ir = 0             #instruction register/currently executing instruction
        self.halted = False
        self.instruction = {    #cpu instruction set and their methods
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
        }

    def load(self, program=[]):
        #strip out all function instructions
        instructions = []
        for line in program:
            line = line.strip()
            instruction = line.split('#')[0]
            if instruction == '': continue
            instructions.append(int(instruction, 2))
        if not len(instructions): self.halted = True
        #insert instructions into ram
        address = 0
        for instruction in instructions:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, MAR): #memory address register
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def LDI(self):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3
    def PRN(self):
        print(self.reg[self.ram_read(self.pc+1)])
        self.pc += 2
    def HLT(self):
        self.halted = True
        self.pc += 1
    def MUL(self):
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            IR = self.ram_read(self.pc)
            self.instruction[IR]()