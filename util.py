

def bits2int(bitString, littleEndian=True, wordSize=8):
    # unsigned
    if len(bitString) != wordSize:
        raise ValueError("bit string is wrong size")
    accum = 0
    for i in range(wordSize):
        index = i if littleEndian else wordSize - 1 - i
        accum += 2**i if bitString[index] else 0
    return accum


def int2bits(x, littleEndian=True, wordSize=8):
    if x < 0:
        raise ValueError("negative value")
    out = [0 for _ in range(wordSize)]
    for i in reversed(range(wordSize)):
        if x >= 2**i:
            x -= 2**i
            index = i if littleEndian else wordSize - 1 - i
            out[index] = 1
    return out

