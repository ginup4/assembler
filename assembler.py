import sys

pins = {
    "bus0": (0, "bus 0"),
    "bus1": (1, "bus 1"),
    "bus2": (2, "bus 2"),
    "bus3": (3, "bus 3"),
    "bus4": (4, "bus 4"),
    "bus5": (5, "bus 5"),
    "bus6": (6, "bus 6"),
    "bus7": (7, "bus 7"),
    "halt": (8, "halt"),
    "inc": (9, "increment"),
    "goto": (10, "goto"),
    "ain": (11, "a in"),
    "aout": (12, "a out"),
    "mod0": (13, "mod 0"),
    "mod1": (14, "mod 1"),
    "alu": (15, "ALU out"),
    "bin": (16, "b in"),
    "bout": (17, "b out"),
    "cin": (18, "c in"),
    "cout": (19, "c out"),
    "din": (20, "d in"),
    "dout": (21, "d out"),
    "usr": (22, "user out"),
    "if0": (23, "if addr 0"),
    "if1": (24, "if addr 1"),
    "if2": (25, "if addr 2"),
    "busif": (26, "bus if"),
    "rng": (27, "RNG out"),
    "tgl": (28, "screen toggle"),
    "clr": (29, "screen reset"),
    "hexdisp": (30, "hex display in"),
    "bindisp": (31, "bin display in"),
    "ramin": (32, "RAM in"),
    "ramout": (33, "RAM out"),
    "ramaddr": (34, "RAM address in"),
    "push": (35, "stack push"),
    "pop": (36, "stack pop"),
    "stackout": (37, "stack out")
}

commands = []
output = []
addresses = {}


def parse():
    with open("input.txt", "r") as file:
        while line := file.readline():
            commands.append(line.split())


def big_indexes():
    global output
    output = list(range(1, len(commands) + 1))


def command(bigi, statement):
    cmd = statement[0]

    if cmd == "rga":
        i = output.index(bigi)
        output.insert(i + 1, ["ain"])
        argument(i + 1, statement[1])

    elif cmd == "rgb":
        pass
    elif cmd == "rgc":
        pass
    elif cmd == "rgd":
        pass
    elif cmd == "ram":
        pass
    elif cmd == "push":
        pass
    elif cmd == "pop":
        pass
    elif cmd == "halt":
        pass
    elif cmd == "hex":
        pass
    elif cmd == "bin":
        pass
    elif cmd == "tgl":
        pass
    elif cmd == "clr":
        pass
    elif cmd == "cpif":
        pass
    elif cmd == "valif":
        pass
    else:
        print("invalid command:", cmd)
        sys.exit()


def argument(smalli, arg):
    if arg.isdecimal():
        output[smalli].extend(int_to_pins(int(arg)))

    elif arg[0] == "#":
        output[smalli].extend(int_to_pins(int(arg[1:], 16)))

    elif arg[0] == "$":
        output[smalli].extend(int_to_pins(int(arg[1:], 2)))

    elif arg[0] == "@":
        output[smalli].append(int(arg[1:]))

    elif arg[:3] == "rga":
        output[smalli].append("aout")
        if len(arg) > 3:
            if arg[3:] == "<<":
                output[smalli].append("mod1")
            elif arg[3:] == ">>":
                output[smalli].append("mod0")
            elif arg[3:] == "!":
                output[smalli].extend(["mod0", "mod1"])
            else:
                print("no such modifier:", arg[3:])
                sys.exit()

    elif arg == "rgb":
        output[smalli].append("bout")

    elif arg == "rgc":
        output[smalli].append("cout")

    elif arg == "rgd":
        output[smalli].append("dout")

    elif arg[:3] == "alu":
        output[smalli].append("alu")
        if arg[3:] == "+":
            pass
        elif arg[3:] == "|":
            output[smalli].append("mod0")
        elif arg[3:] == "<=":
            output[smalli].append("mod1")
        elif arg[3:] == "==":
            output[smalli].extend(["mod0", "mod1"])
        else:
            print("no such modifier:", arg[3:])
            sys.exit()

    elif arg[:4] == "ram:":
        output[smalli].append("ramout")
        output.insert(smalli, ["ramaddr"])
        argument(smalli, arg[4:])

    elif arg == "stack":
        output[smalli].append("stackout")

    else:
        print("invalid argument:", arg)
        sys.exit()


def int_to_pins(i):
    ret = []
    for bit in range(8):
        if (i // 2 ** bit) % 2 == 1:
            ret.append("bus" + str(bit))
    return ret


def move_addresses():
    for i in range(len(output)):
        try:
            if type(output[i]) is int:
                addresses[output.pop(i)] = i
        except IndexError:
            break


def translate_addresses(line):
    for pin in line:
        if type(pin) is int:
            line.extend(int_to_pins(addresses[pin]))
            line.remove(pin)


def save():
    with open("output.txt", "w") as file:
        for line in output:
            translate_addresses(line)
            line = [pins[pin] for pin in line]
            line.sort()
            line = [pin[1] for pin in line]

            print(*line, sep=", ", file=file)


def main():
    parse()
    big_indexes()
    for i, statement in enumerate(commands):
        command(i + 1, statement)
    move_addresses()
    save()


if __name__ == "__main__":
    main()
