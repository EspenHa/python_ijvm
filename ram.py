
import array
from util import int2bits, bits2int

class RAM:

    def __init__(self, mar, mdr, pc, mbr, mir, size=2048):
        self.mar = mar
        self.mdr = mdr
        self.pc  = pc
        self.mbr = mbr
        self.mir = mir

        self.array = array.array('B', [0 for _ in range(size)])

        # list of operations to do, from previous tick
        self.todo = []

    def tick(self):
        # do everything from last tick
        for op in self.todo:
            op()
        self.todo = []

        if self.mir.val[4]:
            self.todo.append(self.fetch)
            # copy current value
            self.pc.old_val = list(self.pc.val)
        if self.mir.val[5]:
            self.todo.append(self.read)
            # copy current value
            self.mar.old_read_val = list(self.mar.val)
        if self.mir.val[6]:
            self.todo.append(self.write)
            # copy current value
            self.mar.old_write_val = list(self.mar.val)
            self.mdr.old_val = list(self.mdr.val)

    def fetch(self):
        self.mbr.val = int2bits(self.array[bits2int(self.pc.old_val, wordSize=32)], wordSize=8)

    def read(self):
        word_start = 4*bits2int(self.mar.old_read_val, wordSize=32)
        word = self.array[word_start:word_start+4]
        self.mdr.val = int2bits(word[0], wordSize=8) + \
                       int2bits(word[1], wordSize=8) + \
                       int2bits(word[2], wordSize=8) + \
                       int2bits(word[3], wordSize=8)

    def write(self):
        word_start = 4*bits2int(self.mar.old_write_val, wordSize=32)
        self.array[word_start+0] = bits2int(self.mdr.old_val[ 0: 8], wordSize=8)
        self.array[word_start+1] = bits2int(self.mdr.old_val[ 8:16], wordSize=8)
        self.array[word_start+2] = bits2int(self.mdr.old_val[16:24], wordSize=8)
        self.array[word_start+3] = bits2int(self.mdr.old_val[24:32], wordSize=8)


if __name__ == "__main__":

    from register import Register

    mir = Register("MIR", 36, None, None, None)

    mar = Register("MAR", 32, None, None, mir)
    mdr = Register("MDR", 32, None, None, mir)
    pc  = Register("PC" , 32, None, None, mir)
    mbr = Register("MBR", 8 , None, None, mir)

    ram = RAM(mar, mdr, pc, mbr, mir, size=16)

    # set write, set mar addr, set value
    mir.val[6] = 1
    mar.val = int2bits(0, wordSize=32)
    mdr.val = int2bits(0xFF0014, wordSize=32)
    ram.tick()
    print(ram.array)
    print(list(reversed(mdr.val)))

    mir.val[6] = 0
    # set read, set mar addr, reset mdr
    mir.val[5] = 1
    mar.val = int2bits(0, wordSize=32)
    mdr.val = int2bits(0, wordSize=32)
    ram.tick()
    print(ram.array)
    print(list(reversed(mdr.val)))

    mir.val[5] = 0
    # the value is now back in mdr
    ram.tick()
    print(ram.array)
    print(list(reversed(mdr.val)))

    # fetch
    mir.val[4] = 1
    pc.val = int2bits(0, wordSize=32)
    print(ram.array)
    print(list(reversed(mbr.val)))
    ram.tick()

    # 0x14 is now in MBR, fetch another
    mir.val[4] = 1
    pc.val = int2bits(2, wordSize=32)
    ram.tick()
    print(ram.array)
    print(list(reversed(mbr.val)))

    # 0xFF is now in MBR
    mir.val[4] = 0
    ram.tick()
    print(ram.array)
    print(list(reversed(mbr.val)))
