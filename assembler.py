from ijvm import inst_set


def assemble_simple(assembly_code):
    machine_code = []

    for line in assembly_code.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        comment_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]

        # opcode
        parts = line.split()
        opcode = inst_set[parts[0]]
        machine_code.append(opcode.hex_val)

        # operands
        for part in parts[1:]:
            if not part:
                continue
            machine_code.append(int(part))

    return machine_code


def int2twos_complement(x):
    if x >= 0:
        pass
    else:
        pass
