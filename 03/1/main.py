import argparse


def is_next_to_symbol(x, y, table):
    # print("number", table[y][x])
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                y + j >= 0
                and y + j < len(input_)
                and x + i >= 0
                and x + i < len(input_[0])
            ):
                element = table[y + j][x + i]
                # print(f"({i}, {j})", element)
                if element != "." and not element.isdigit():
                    # print("surrounds not clear")
                    return True
    # print("surrounds clear")
    return False


def get_parts(table):
    parts = []
    acc = ""
    is_part = False
    for l, line in enumerate(table):
        if len(acc) > 0:
            if is_part:
                parts.append(int(acc))
            acc = ""
            is_part = False
        for i, c in enumerate(line):
            if c.isdigit():
                acc += c
                if is_next_to_symbol(i, l, table):
                    is_part = True
            elif len(acc) > 0:
                if is_part:
                    parts.append(int(acc))
                acc = ""
                is_part = False
            else:
                continue
    return parts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get digits",
    )
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        input_ = f.readlines()

    parts = get_parts(input_)
    input_ = [line.strip("\n") for line in input_]
    parts_strip = get_parts(input_)
    print(parts)
    print(parts_strip)
    print(len(parts))
    print(len(parts_strip))
    print(sum(parts))
    print(sum(parts_strip))
