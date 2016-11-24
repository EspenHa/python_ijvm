from ijvm import inst_set


def assemble(assembly_code):
    label2index = dict()

    index = 0

    for line in assembly_code.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        comment_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]

        parts = line.split()

        colon_index = parts[0].find(':')
        if colon_index != -1:
            label = parts[0][:colon_index]
            # off by one ?
            label2index[label] = index
        else:
            index += len(parts)

    index = 0
    pure_assembly = []

    for line in assembly_code.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        comment_index = line.find('#')
        if comment_index != -1:
            line = line[:comment_index]

        inst = []
        parts = line.split()

        colon_index = parts[0].find(':')
        if colon_index != -1:
            continue
        else:
            inst.append(parts[0])
            for part in line[1:]:
                if not part:
                    continue
                if part in label2index:
                    # operand is label
                    assert len(line) == 2
                    label_index = label2index[part]
                    # off by one ?
                    offset = label_index - index
                    inst.extend(int2twos_complement(offset))
                else:
                    inst.append(part)

        index += len(inst)
        pure_assembly.append(inst)
            
    return assemble_simple(assembly_code)


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
