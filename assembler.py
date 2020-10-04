pins = {
    "bus0": (0, "bus 0"),
    "bus1": (1, "bus 1"),
    "bus2": (2, "bus 2"),
    "bus3": (3, "bus 2"),
    "bus4": (4, "bus 2"),
    "bus5": (5, "bus 2"),
    "bus6": (6, "bus 2"),
    "bus7": (7, "bus 2"),
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


def main():
    with open("input.txt", "r") as file:
        while line := file.readline():
            cmd, *args = line.split()


if __name__ == "__main__":
    main()
