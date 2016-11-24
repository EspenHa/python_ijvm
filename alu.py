from collections import namedtuple

from shifter import Shifter
from util import bits2int

alu_inst = namedtuple("ALU_instruction", ["bit_string", "name"])

#                                           f0   f1   enA  enB invA  inc
operations = {0x18 : alu_inst(list(reversed([0,   1,   1,   0,   0,   0])), "A"      ),
              0x14 : alu_inst(list(reversed([0,   1,   0,   1,   0,   0])), "B"      ),
              0x1A : alu_inst(list(reversed([0,   1,   1,   0,   1,   0])), "NOT A"  ),
              0x2C : alu_inst(list(reversed([1,   0,   1,   1,   0,   0])), "NOT B"  ),
              0x3C : alu_inst(list(reversed([1,   1,   1,   1,   0,   0])), "A+B"    ),
              0x3D : alu_inst(list(reversed([1,   1,   1,   1,   0,   1])), "A+B+1"  ),
              0x39 : alu_inst(list(reversed([1,   1,   1,   0,   0,   1])), "A+1"    ),
              0x35 : alu_inst(list(reversed([1,   1,   0,   1,   0,   1])), "B+1"    ),
              0x3F : alu_inst(list(reversed([1,   1,   1,   1,   1,   1])), "B-A"    ),
              0x36 : alu_inst(list(reversed([1,   1,   0,   1,   1,   0])), "B-1"    ),
              0x3B : alu_inst(list(reversed([1,   1,   1,   0,   1,   1])), "-A"     ),
              0x0C : alu_inst(list(reversed([0,   0,   1,   1,   0,   0])), "A AND B"),
              0x1C : alu_inst(list(reversed([0,   1,   1,   1,   0,   0])), "A OR B" ),
              0x10 : alu_inst(list(reversed([0,   1,   0,   0,   0,   0])), "0"      ),
              0x31 : alu_inst(list(reversed([1,   1,   0,   0,   0,   1])), "1"      ),
              0x32 : alu_inst(list(reversed([1,   1,   0,   0,   1,   0])), "-1"     )}

class ALU:
    class ALU_bit:

        @staticmethod
        def execute(a, b, f0, f1, enA, enB, invA, carry_in):

            en0, en1, en2, en3 = ALU.ALU_bit.decode_f(f0, f1)

            logical_in_A = invA ^ (a and enA) # ^ is XOR
            logical_in_B = b and enB

            out0, out1, out2 = ALU.ALU_bit.decode_logical(logical_in_A, logical_in_B, en0, en1, en2)

            out3, carry_out = ALU.ALU_bit.fullAdd(logical_in_A, logical_in_B, en3, carry_in)

            return out0 or out1 or out2 or out3, carry_out

        @staticmethod
        def decode_f(f0, f1):
            return (not f0 and not f1,
                    not f0 and     f1,
                        f0 and not f1,
                        f0 and     f1)

        @staticmethod
        def decode_logical(logA, logB, en0, en1, en2):
            return (en0 and (logA and logB),
                    en1 and (logA or  logB),
                    en2 and   int(not logB))

        @staticmethod
        def fullAdd(logA, logB, en3, carry_in):
            return (en3 and ((logA ^ logB) ^ carry_in), # sum
                   (en3 and logA and logB) or (en3 and (logA ^ logB) and carry_in)) # carry


    def __init__(self, busA, busB, busC, mir):

        # busses
        self.A = busA
        self.B = busB
        self.shifter = Shifter(busC, mir)
        self.mir = mir

        # flags
        self.N = None
        self.Z = None


    def tick(self):

        # control lines
        inc  = self.mir.val[16]
        invA = self.mir.val[17]
        enB  = self.mir.val[18]
        enA  = self.mir.val[19]
        f1   = self.mir.val[20]
        f0   = self.mir.val[21]

        out = []
        self.Z = 0

        for bitA, bitB in zip(self.A.val, self.B.val):

            out_bit, carry = self.ALU_bit.execute(bitA, bitB,
                                                  f0,   f1,
                                                  enA,  enB,
                                                  invA, inc)
            self.Z = self.Z or out_bit  # keep track of if there is a 1
            inc = carry                 # set inc for next bit
            out.append(out_bit)         # build word from bits

        self.N = out[-1]
        self.Z = int(not(self.Z))

        self.shifter.shift_and_write_to_bus(out)

    def get_last_instruction_name(self):
        x = bits2int(self.mir.val[16:22], wordSize=6)
        if x in operations:
            return operations[x].name
        else:
            return "UNKNOWN"

    @staticmethod
    def test_operations(intA, intB):
        from util import bits2int, int2bits
        from register import Register
        from bus import Bus

        A = Bus("A", 32)
        B = Bus("B", 32)
        C = Bus("C", 32)

        mir = Register("MIR", 36, None, None, None)

        alu = ALU(A, B, C, mir)


        wordSize = max(intA.bit_length(), intB.bit_length())
        A.val = int2bits(intA, wordSize)
        B.val = int2bits(intB, wordSize)

        print("A = binary({0}) -> {1}".format(intA, list(reversed(A.val))))
        print("B = binary({0}) -> {1}".format(intB, list(reversed(B.val))))
        print()


        for _, op in operations.items():
            mir.val = [0 for _ in range(16)] + op.bit_string + [0 for _ in range(16+6, 36)]

            alu.tick()

            sol = C.val

            print("f(A,B) = {0}".format(op.name))
            print("binary({0}) -> {1}".format(bits2int(sol), list(reversed(sol))))
            print()

if __name__ == "__main__":
    ALU.test_operations(4, 1)
