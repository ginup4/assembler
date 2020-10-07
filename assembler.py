import sys

pins = {
    "bus0": 44,
    "bus1": 46,
    "bus2": 48,
    "bus3": 50,
    "bus4": 52,
    "bus5": 54,
    "bus6": 56,
    "bus7": 58,
    "halt": 60,
    "inc": 62,
    "goto": 64,
    "ain": 66,
    "aout": 68,
    "mod0": 70,
    "mod1": 72,
    "alu": 74,
    "bin": 76,
    "bout": 78,
    "cin": 80,
    "cout": 82,
    "din": 84,
    "dout": 86,
    "usr": 90,
    "if0": 92,
    "if1": 94,
    "if2": 96,
    "busif": 98,
    "rng": 102,
    "tgl": 104,
    "clr": 106,
    "hexdisp": 108,
    "bindisp": 110,
    "ramin": 112,
    "ramout": 114,
    "ramaddr": 116,
    "push": 118,
    "pop": 120,
    "stackout": 122
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
    i = output.index(bigi)

    if cmd == "rga":
        output.insert(i + 1, ["ain"])
        argument(i + 1, statement[1])

    elif cmd == "rgb":
        output.insert(i + 1, ["bin"])
        argument(i + 1, statement[1])

    elif cmd == "rgc":
        output.insert(i + 1, ["cin"])
        argument(i + 1, statement[1])

    elif cmd == "rgd":
        output.insert(i + 1, ["din"])
        argument(i + 1, statement[1])

    elif cmd == "ram":
        output.insert(i + 1, ["ain"])
        output.insert(i + 2, ["ramaddr"])
        output.insert(i + 3, ["ramin", "aout"])
        argument(i + 2, statement[1], "rga")
        argument(i + 1, statement[2])

    elif cmd == "push":
        output.insert(i + 1, ["push"])
        argument(i + 1, statement[1])

    elif cmd == "pop":
        output.insert(i + 1, ["pop"])

    elif cmd == "hex":
        output.insert(i + 1, ["hexdisp"])
        argument(i + 1, statement[1])

    elif cmd == "bin":
        output.insert(i + 1, ["bindisp"])
        argument(i + 1, statement[1])

    elif cmd == "tgl":
        output.insert(i + 1, ["tgl"])
        argument(i + 1, statement[1])

    elif cmd == "clr":
        output.insert(i + 1, ["clr"])

    elif cmd == "halt":
        output.insert(i + 1, ["halt", "goto"])
        if len(statement) > 1:
            argument(i + 1, statement[1])

    elif cmd == "cpif":
        pass

    elif cmd == "valif":
        output.insert(i + 1, ["busif"] + int_to_pins(int(statement[3]), 3, "if"))
        output.insert(i + 2, ["goto", bigi + 1])
        output.insert(i + 3, ["goto"])

        argument(i + 3, statement[1])
        argument(i + 1, statement[2])

    else:
        print("invalid command:", cmd)
        sys.exit()


def argument(smalli, arg, *illegal):

    if arg.isdecimal():
        output[smalli].extend(int_to_pins(int(arg)))

    elif arg[0] == "#":
        output[smalli].extend(int_to_pins(int(arg[1:], 16)))

    elif arg[0] == "$":
        output[smalli].extend(int_to_pins(int(arg[1:], 2)))

    elif arg[0] == "@":
        output[smalli].append(int(arg[1:]))

    elif arg[:3] == "rga":
        if "rga" in illegal:
            illegal_argument(arg)
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
        if "rgb" in illegal:
            illegal_argument(arg)
        output[smalli].append("bout")

    elif arg == "rgc":
        if "rgc" in illegal:
            illegal_argument(arg)
        output[smalli].append("cout")

    elif arg == "rgd":
        if "rgd" in illegal:
            illegal_argument(arg)
        output[smalli].append("dout")

    elif arg[:3] == "alu":
        if "alu" in illegal:
            illegal_argument(arg)
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
        if "ram" in illegal:
            illegal_argument(arg)
        output[smalli].append("ramout")
        output.insert(smalli, ["ramaddr"])
        argument(smalli, arg[4:])

    elif arg == "stack":
        if "stack" in illegal:
            illegal_argument(arg)
        output[smalli].append("stackout")

    elif arg == "rng":
        if "rng" in illegal:
            illegal_argument(arg)
        output[smalli].append("rng")

    elif arg == "usr":
        if "usr" in illegal:
            illegal_argument(arg)
        output[smalli].append("usr")

    else:
        print("invalid argument:", arg)
        sys.exit()


def illegal_argument(arg):
    print("illegal argument:", arg)
    sys.exit()


def int_to_pins(i, n=8, pin="bus"):
    ret = []
    for bit in range(n):
        if (i // 2 ** bit) % 2 == 1:
            ret.append(pin + str(bit))
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
            break


def save():
    if len(output) > 128:
        print(f"not enough space in program memory for {len(output)} commands")
    with open("output.mcfunction", "w") as file:
        for i, line in enumerate(output):
            translate_addresses(line)
            line = [pins[pin] for pin in line]
            line.sort()

            for pin in line:
                print("setblock", pin, 65 - 5 * (i // 32), 29 - 3 * (i % 32), "minecraft:redstone_wall_torch", "replace", file=file)


def main():
    parse()
    big_indexes()
    for i, statement in enumerate(commands):
        command(i + 1, statement)
    print(*output, sep="\n")
    move_addresses()
    print(*output, sep="\n")
    print(addresses)
    save()


if __name__ == "__main__":
    main()
