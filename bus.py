
class Bus:

    def __init__(self, name, width):

        self.name = name

        # initialize value
        self.val = [0 for _ in range(width)]

    #other objects read/write to Bus.val directly
