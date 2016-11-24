from collections import namedtuple

from alu import ALU
from register import Register
from bus import Bus
from control import Control
from ram import RAM

ijvm_inst = namedtuple("IJVM_instruction", ["bit_string", "name", "hex_val", "n_micro"])

inst_set = {"BIPUSH"        : ijvm_inst(list(reversed([0, 0, 0, 1,  0, 0, 0, 0])), "BIPUSH"       , 0x10,  3),
            "DUP"           : ijvm_inst(list(reversed([0, 1, 0, 1,  1, 0, 0, 1])), "DUP"          , 0x59,  2),
            "GOTO"          : ijvm_inst(list(reversed([1, 0, 1, 0,  0, 1, 1, 1])), "GOTO"         , 0xA7,  6),
            "IADD"          : ijvm_inst(list(reversed([0, 1, 1, 0,  0, 0, 0, 0])), "IADD"         , 0x60,  3),
            "IAND"          : ijvm_inst(list(reversed([0, 1, 1, 1,  1, 1, 1, 0])), "IAND"         , 0x7E,  3),
            "IFEQ"          : ijvm_inst(list(reversed([1, 0, 0, 1,  1, 0, 0, 1])), "IFEQ"         , 0x99,  4),
            "IFLT"          : ijvm_inst(list(reversed([1, 0, 0, 1,  1, 0, 1, 1])), "IFLT"         , 0x9B,  4),
            "IF_ICMPEQ"     : ijvm_inst(list(reversed([1, 0, 0, 1,  1, 1, 1, 1])), "IF_ICMPEQ"    , 0x9F,  6),
            "IINC"          : ijvm_inst(list(reversed([1, 0, 0, 0,  0, 1, 0, 0])), "IINC"         , 0x84,  6),
            "ILOAD"         : ijvm_inst(list(reversed([0, 0, 0, 1,  0, 1, 0, 1])), "ILOAD"        , 0x15,  5),
            "INVOKEVIRTUAL" : ijvm_inst(list(reversed([1, 0, 1, 1,  0, 1, 1, 0])), "INVOKEVIRTUAL", 0xB6, 22),
            "IOR"           : ijvm_inst(list(reversed([1, 0, 0, 0,  0, 0, 0, 0])), "IOR"          , 0x80,  3),
            "IRETURN"       : ijvm_inst(list(reversed([1, 0, 1, 0,  1, 1, 0, 0])), "IRETURN"      , 0xAC,  8),
            "ISTORE"        : ijvm_inst(list(reversed([0, 0, 1, 1,  0, 1, 1, 0])), "ISTORE"       , 0x36,  6),
            "ISUB"          : ijvm_inst(list(reversed([0, 1, 1, 0,  0, 1, 0, 0])), "ISUB"         , 0x64,  3),
            "LDC_W"         : ijvm_inst(list(reversed([0, 0, 0, 1,  0, 0, 1, 1])), "LDC_W"        , 0x13,  4),
            "NOP"           : ijvm_inst(list(reversed([0, 0, 0, 0,  0, 0, 0, 0])), "NOP"          , 0x00,  1),
            "POP"           : ijvm_inst(list(reversed([0, 1, 0, 1,  0, 1, 1, 1])), "POP"          , 0x57,  3),
            "SWAP"          : ijvm_inst(list(reversed([0, 1, 0, 1,  1, 1, 1, 1])), "SWAP"         , 0x5F,  6),
            "WIDE"          : ijvm_inst(list(reversed([1, 1, 0, 0,  0, 1, 0, 0])), "WIDE"         , 0xC4,  2)}


class IJVM:

    def __init__(self):

        # 32 bit wide buses
        self.A = Bus("A", 32)
        self.B = Bus("B", 32)
        self.C = Bus("C", 32)

        # mir is a special 36 bit register
        self.mir = Register("MIR", 36, None, None, None)

        # arithmetic logic unit
        # creates its own shifter unit
        self.alu = ALU(self.A, self.B, self.C, self.mir)

        # registers
        self.registers = {"MAR" : Register("MAR", 32, None  , self.C, self.mir), # Memory Adress Register
                          "MDR" : Register("MDR", 32, self.B, self.C, self.mir), # Memory Data Register
                          "PC"  : Register("PC" , 32, self.B, self.C, self.mir), # Program Counter
                          "MBR" : Register("MBR",  8, self.B, None  , self.mir), # Memory Byte Register
                          "SP"  : Register("SP" , 32, self.B, self.C, self.mir), # Stack Pointer
                          "LV"  : Register("LV" , 32, self.B, self.C, self.mir), # Local Variable
                          "CPP" : Register("CPP", 32, self.B, self.C, self.mir), # Constant Pool Pointer
                          "TOS" : Register("TOS", 32, self.B, self.C, self.mir), # Top Of Stack
                          "OPC" : Register("OPC", 32, self.B, self.C, self.mir), # OPCode
                          "H"   : Register("H"  , 32, self.A, self.C, self.mir)}



        # control unit
        self.control = Control(self.registers["MBR"], self.mir, self.alu)

        # 2KB RAM
        self.ram = RAM(self.registers["MAR"],
                       self.registers["MDR"],
                       self.registers["PC"],
                       self.registers["MBR"],
                       self.mir)

    def tick(self, verbose=True):

        if verbose:
            print("SP\t", bits2int(self.registers["SP"].val, wordSize=32), end='\t->\t')
            print("RAM[4*SP]\t",self.ram.array[4*bits2int(ijvm.registers["SP"].val, wordSize=32)])

            print("LV\t", bits2int(self.registers["LV"].val, wordSize=32), end='\t->\t')
            print("RAM[4*LV]\t", self.ram.array[4*bits2int(ijvm.registers["LV"].val, wordSize=32)])

            print("MAR\t", bits2int(self.registers["MAR"].val, wordSize=32), end='\t->\t')
            print("RAM[4*MAR]\t", self.ram.array[4*bits2int(self.registers["MAR"].val, wordSize=32)])

            print("PC\t", bits2int(self.registers["PC"].val, wordSize=32), end='\t->\t')
            print("RAM[PC]\t\t",self.ram.array[bits2int(self.registers["PC"].val, wordSize=32)])

            print("MDR\t", bits2int(self.registers["MDR"].val, wordSize=32))

            print("TOS\t", bits2int(self.registers["TOS"].val, wordSize=32))

            print("MBR\t", bits2int(self.registers["MBR"].val, wordSize=8))

            print("OPC\t", bits2int(self.registers["OPC"].val, wordSize=32))

            print("H\t", bits2int(self.registers["H"].val, wordSize=32))

            print("Z-flag\t", self.alu.Z)
            print("N-flag\t", self.alu.N)
            print()

        if verbose:
            current_micro_instruction, mal = self.control.get_micro_instruction_name()
            print("Current microinstruction is\t\t{0}".format(current_micro_instruction))
            print("MAL for this microinstruction is\t{0}".format(mal))


        for reg in self.registers.values():
            reg.set_write_pin()
            reg.write_to_bus()
            if verbose and reg.write and reg.name != "H":
                print("Wrote from register\t\t\t{0} to {1}-bus".format(reg.name, reg.write_bus.name))

            # need to set read pins so they dont get overwriten by a new value in MIR
            reg.set_read_pin()

        self.alu.tick()
        if verbose:
            print("ALU performed \t\t\t\tf = {0}".format(self.alu.get_last_instruction_name()))

        for reg in self.registers.values():
            reg.read_from_bus()
            if verbose and reg.read:
                print("Wrote from \t\t\t\t{1}-bus to {0}".format(reg.name, reg.read_bus.name))

        self.ram.tick()
        if verbose and len(self.ram.todo) != 0:
            for op in self.ram.todo:
                print("Sent {0} to RAM".format(op.__name__))

        self.control.tick()
        if verbose:
            print("Loaded new\t\t\t\taddress {0} into MPC".format(self.control.get_address()))

        if verbose:
            print()


if __name__ == "__main__":
    from util import int2bits, bits2int
    from assembler import assemble, assemble_simple

    ijvm = IJVM()
    assembly_code = """
                    BIPUSH 1

                    IFEQ ELSE

                    BIPUSH 2
                    GOTO END

                    ELSE:
                    BIPUSH 3

                    END:
                    """

    sum_to_n      = """
                    # var0 = 7
                    BIPUSH 7
                    ISTORE 100

                    # var1 = 0
                    BIPUSH 0
                    ISTORE 101

                    # if var0 == 0
                    ILOAD 100
                    IFEQ 0 20

                    # var1 = var0 + var1
                    ILOAD 100
                    ILOAD 101
                    IADD
                    ISTORE 101

                    # var0 -= 1
                    ILOAD 100
                    BIPUSH 1
                    ISUB
                    ISTORE 100

                    # goto if statment (- 19 instructions == 0xFFED)
                    GOTO 255 237
                    ILOAD 101
                    """

    easy_to_do = """
                 BIPUSH 4
                 ISTORE 100 # have to put the variable somewhere the stack will probably never go to
                 BIPUSH 3
                 ISTORE 101
                 ILOAD 100
                 ILOAD 101
                 IADD
                 ISTORE 102
                 ILOAD 102
                 BIPUSH 7
                 IF_ICMPEQ 0 15
                 ILOAD 100
                 BIPUSH 1
                 ISUB
                 ISTORE 100
                 BIPUSH 2 # return code to indicate where we branched
                 GOTO 0 9
                 BIPUSH 0
                 ISTORE 101
                 BIPUSH 1 # return code to indicate where we branched
                 """
    machine_code = assemble_simple(sum_to_n)
    prog_start_index = 4


    machine_code.append(0xFF)
    # will cause KeyError in dict lookup
    # this means the program is finished

    for index, number in enumerate(machine_code):
        ijvm.ram.array[prog_start_index + index] = number

    # set program counter and memory byte register to first instruction
    # this has to be present before the program starts
    ijvm.registers["PC"].val = int2bits(prog_start_index, wordSize=32)
    ijvm.registers["MBR"].val = int2bits(ijvm.ram.array[prog_start_index], wordSize=8)

    # set stack pointer to an empty location, (multiple of 4)
    ijvm.registers["SP"].val = int2bits(4*((prog_start_index + len(machine_code))//4 + 1), wordSize=32)

    verbose = False
    debug = False
    try:
        while True:
            ijvm.tick(verbose or debug)
            if debug:
                input()
    except KeyError as e:

        if verbose or debug:
            print()

        if e.args[0] == 0xFF or e.args[0] == 0x1FF:
            # this is the end of the program
            # final output is in top of stack
            print("OUTPUT", bits2int(ijvm.registers["TOS"].val, wordSize=32))
        else:
            # something wrong happened
            # probably a GOTO jumping to data instead of an instruction
            print("ERROR")
            print("Tried to jump to microinstruction {0}, but there is no such microinstruction".format(e))

