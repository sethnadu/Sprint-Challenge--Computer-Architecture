"""CPU functionality."""

import sys

# LOAD immediate 130
LDI = 0b10000010 
# Print 71
PRN = 0b01000111 
# Multiply 162
MUL = 0b10100010
# Add 160
ADD = 0b10100000
# PUSH 69
PUSH = 0b01000101
# POP 70
POP = 0b01000110
# Call register 80
CALL = 0b01010000
# Return from subrouting 17
RET = 0b00010001
# Halt 1
HTL = 0b00000001 
    
# SPRINT MVP
# CMP 167
CMP = 0b10100111
# JMP 84
JMP = 0b01010100
# JNE check if not equal flag 86
JNE = 0b01010110
# JEQ check if equal flag 85
JEQ = 0b01010101

# SPRINT STRETCH
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        # Start at top, index 7 of 8-bit
        self.sp = 7
        self.flag = 0b00000000
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[ADD] = self.handle_add
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret

        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JNE] = self.handle_jne
        self.branchtable[JEQ] = self.handle_jeq

        self.branchtable[AND] = self.handle_and
        self.branchtable[OR] = self.handle_or
        self.branchtable[XOR] = self.handle_xor
        self.branchtable[NOT] = self.handle_not

    def load(self, fileName):
        """Load a program into memory."""
        address = 0
        binary_strings = []
        program = []

        #  If second arguement is valid
        try:
            # Open the file that contains the programs
            l = open(fileName, 'r')
            for line in l:
                if line.startswith('#'):
                    None
                elif line == '\n':
                    None
                elif line.startswith('\n'):
                    None
                else:
                    binary_strings.append(line)

            print("Array of Binary_strings", binary_strings)
            
            for i in binary_strings:
                comment_split = i.split('#')
                new_value = comment_split[0]
                x = int(new_value, 2)
                program.append(x)
                
            print('program', program)
            for instruction in program:
                # self.ram[address] = instruction
                self.ram_write(address, instruction)
                address += 1

        # If second arguement is invalid
        except FileNotFoundError:
            print(f'{sys.argv[0]} : {sys.argv[1]} Not found')
            sys.exit(2)

    def ram_read(self, MAR):
        # print(self.ram[MAR])
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def handle_ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b

    def handle_prn(self, reg_a, unused):
        print("REG", self.reg[reg_a])
 
    def handle_mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
    
    def handle_add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)

    def handle_or(self, reg_a, reg_b):
        self.alu("OR", reg_a, reg_b)
    
    def handle_and(self, reg_a, reg_b):
        self.alu("AND", reg_a, reg_b)

    def handle_xor(self, reg_a, reg_b):
        self.alu("XOR", reg_a, reg_b)

    def handle_not(self, reg_a, reg_b):
        self.alu("NOT", reg_a, reg_b)

    def handle_cmp(self, reg_a, reg_b):
        self.alu("CMP", reg_a, reg_b)
    
    def handle_push(self, reg_a, unused):
        # Decrement the SP
        self.reg[self.sp] -= 1
        value = self.reg[reg_a]
        # Copy value of register to self.reg[reg_a]
        self.ram_write(self.reg[self.sp], value)

    def handle_pop(self, reg_a, unused):
        # set register's address(reg_a) to what the current ram's-registers SP is
        value = self.ram_read(self.reg[self.sp])
        self.reg[reg_a] = value
        # Increment the sp
        self.reg[self.sp] += 1

    def handle_call(self):
        # print('call')
        value = self.pc + 2
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], value)
        reg = self.ram_read(self.pc + 1)
        subroutine_address = self.reg[reg]
        self.pc = subroutine_address
        
    def handle_ret(self):
        # print('ret')
        return_address = self.reg[self.sp]
        self.pc = self.ram_read(return_address)
        self.reg[self.sp] +=1
        
    def handle_jmp(self):
        reg = self.ram_read(self.pc + 1)
        jump_address = self.reg[reg]
        self.pc = jump_address

    def handle_jne(self):
        if self.flag != 0b00000001:
            reg = self.ram_read(self.pc + 1)
            jump_address = self.reg[reg]
            self.pc = jump_address
        else: 
            self.pc += 2

    def handle_jeq(self):
        if self.flag == 0b00000001:
            reg = self.ram_read(self.pc + 1)
            jump_address = self.reg[reg]
            self.pc = jump_address
        else:
            self.pc += 2


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            # print(self.reg[reg_a])
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = self.reg[reg_a] != self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")




    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def run(self):
        """Run the CPU."""
        
        running = True
        branch_jump = [CALL, RET, JMP, JNE, JEQ]
        while running:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            ir = self.ram_read(self.pc)
            print(ir)
            if ir in self.branchtable:
                if ir in branch_jump:
                    self.branchtable[ir]()
                else:
                    self.branchtable[ir](operand_a, operand_b)
                    # Use shift to get last two arguements ex in LPI [10]000010
                    # Take the value(num of arguments) add 1 to go to next operation 
                    move = (ir >> 6) + 1
                    self.pc += move
            elif ir is HTL:
                running = False