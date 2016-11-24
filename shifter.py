
class Shifter:

    def __init__(self, write_bus, mir):
        self.write_bus = write_bus
        self.mir = mir

    def shift_and_write_to_bus(self, word):
        # unsure which of the two shifts has precedence

        # sra1 = shift right arithmetic 1
        sra1 = self.mir.val[22]
        # sll8 = shift left logical 8
        sll8 = self.mir.val[23]

        if sll8:
            word = [0 for _ in range(8)] +  word[:-8]
        if sra1:
            word = word[1:] + [word[-1]] # sign extend

        self.write_bus.val = word

