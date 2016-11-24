
class Register:
    read_mir_index = {"MAR" :  7,
                      "MDR" :  8,
                      "PC"  :  9,
                      "SP"  : 10,
                      "LV"  : 11,
                      "CPP" : 12,
                      "TOS" : 13,
                      "OPC" : 14,
                      "H"   : 15}

    write_mir_decoded_index = {"MDR" : 0,
                               "PC"  : 1,
                               "MBR" : 2,
                               "MBRU": 3,
                               "SP"  : 4,
                               "LV"  : 5,
                               "CPP" : 6,
                               "TOS" : 7,
                               "OPC" : 8}

    def __init__(self, name, size, write_bus, read_bus, mir):

        self.name = name

        # only MBR will do sign extension
        self.sign_extend = False

        # all registers except H will have B as write_bus, if write_bus is not None
        self.write_bus = write_bus
        # read_bus will always be C, if read_bus is not None
        self.read_bus = read_bus

        self.val = [0 for _ in range(size)]

        if name != "MIR":
            # all registers, except MIR itself, needs a reference to MIR
            self.mir = mir
        else:
            # define a special function to decode B field, only for MIR
            from util import bits2int
            def decode_B_field():
                x = bits2int(self.val[:4], wordSize=4)
                return [1 if x == i else 0 for i in range(9)]
            self.decode_B_field = decode_B_field


        # initialize control pins
        self.read  = 0
        self.write = 0

        if name == "H":
            # H always writes to A bus
            self.write = 1


    def set_read_pin(self):
        # MBR does not read from C bus
        # MIR is not connected to busses
        if self.name == "MIR" or self.name == "MBR":
            # do not change self.read
            return
        # read MIR from your own index
        mir_index = self.read_mir_index[self.name]
        self.read = self.mir.val[mir_index]

    def set_write_pin(self):
        # H and MAR has no write control pin
        # (always true for H, always false for MAR)
        # MIR is not connected to busses
        if self.name == "MIR" or self.name == "H" or self.name == "MAR":
            # do not change self.write
            return


        # this is a one-hot encoding
        # self.write_mir_decoded_index lets you look up your index
        # this index is used to check the decoded B field
        decoded_B_field = self.mir.decode_B_field()

        if self.name == "MBR":
            # since there is only a MBR object, and no MBRU object, we have to check both
            decoded_index_mbr  = self.write_mir_decoded_index["MBR"]
            decoded_index_mbru = self.write_mir_decoded_index["MBRU"]

            write_mbr  = decoded_B_field[decoded_index_mbr]
            write_mbru = decoded_B_field[decoded_index_mbru]

            if write_mbr:
                self.write = 1
                self.sign_extend = False
            elif write_mbru:
                self.write = 1
                self.sign_extend = True
            else:
                self.write = 0
                self.sign_extend = False
        else:
            decoded_index = self.write_mir_decoded_index[self.name]
            self.write = decoded_B_field[decoded_index]


    def write_to_bus(self):
        if self.write:
            extend_val = self.val[-1] if self.sign_extend else 0
            # there will be no extension if this register is 32 bit wide
            # and self.write will always be false for MIR (36 bits)
            self.write_bus.val = self.val + [extend_val for _ in range(32 - len(self.val))]

    def read_from_bus(self):
        if self.read:
            self.val = self.read_bus.val

