from microinstructions import control_store
from util import bits2int, int2bits

class Control:

    def __init__(self, mbr, mir, alu):

        # refrence to mbr
        self.mbr = mbr

        #refrence to alu, needed for N and Z flag
        self.alu = alu

        #
        self.mir = mir

        # load initial instruction from mbr, high bit is one (main1)
        self.mpc = mbr.val + [1]

        self.updateMIR()

    def tick(self):
        self.load_next_address()
        self.updateMIR()

    def load_next_address(self):

        jamz = self.mir.val[24]
        jamn = self.mir.val[25]
        jmpc = self.mir.val[26]

        nextAddr = self.mir.val[27:-1]

        if jmpc:
            for i in range(len(nextAddr)):
                self.mpc[i] = self.mbr.val[i] or nextAddr[i]
        else:
            for i in range(len(nextAddr)):
                self.mpc[i] = nextAddr[i]

        self.mpc[-1] = self.mir.val[-1] or (self.alu.N and jamn) or (self.alu.Z and jamz)

    def updateMIR(self):
        adr = self.get_address()
        nextMIRparts = control_store[adr][:6]

        next_adr  = int2bits(nextMIRparts[0], wordSize=9)
        jam       = int2bits(nextMIRparts[1], wordSize=3)
        shift_alu = int2bits(nextMIRparts[2], wordSize=8)
        C_field   = int2bits(nextMIRparts[3], wordSize=9)
        mem       = int2bits(nextMIRparts[4], wordSize=3)
        B_field   = int2bits(nextMIRparts[5], wordSize=4)

        self.mir.val = B_field + mem + C_field + shift_alu + jam + next_adr


    def get_address(self):
        return bits2int(self.mpc, wordSize=9) 

    def get_micro_instruction_name(self):
        return control_store[self.get_address()][6:8]

