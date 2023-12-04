import argparse
from functools import reduce
import operator


def find_surrounding_gear(x, y, table):
    surrounding_gears = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                y + j >= 0
                and y + j < len(input_)
                and x + i >= 0
                and x + i < len(input_[0])
            ):
                element = table[y + j][x + i]
                if element == "*":
                    surrounding_gears.add((y + j, x + i))
    return surrounding_gears


def get_parts(table):
    parts = []
    acc = ""
    surrounding_gears = set()
    is_part = False
    for l, line in enumerate(table):
        if len(acc) > 0:
            if is_part:
                parts.append((int(acc), surrounding_gears))
            acc = ""
            surrounding_gears = set()
            is_part = False
        for i, c in enumerate(line):
            if c.isdigit():
                acc += c
                gear_coordinates = find_surrounding_gear(i, l, table)
                if len(gear_coordinates) > 0:
                    is_part = True
                    surrounding_gears |= gear_coordinates
            elif len(acc) > 0:
                if is_part:
                    parts.append((int(acc), surrounding_gears))
                acc = ""
                surrounding_gears = set()
                is_part = False
            else:
                continue
    return parts


def get_gears(parts):
    gear_parts = {}
    for part, gears in parts:
        for gear in gears:
            if gear not in gear_parts:
                gear_parts[gear] = []
            gear_parts[gear].append(part)
    return gear_parts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get digits",
    )
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        input_ = f.readlines()

    input_ = [line.strip("\n") for line in input_]
    parts = get_parts(input_)
    gear_parts = get_gears(parts)
    gear_parts = {gear: parts for gear, parts in gear_parts.items() if len(parts) == 2}
    gear_ratios = [reduce(operator.mul, parts) for parts in gear_parts.values()]

    print(parts)
    print(gear_parts)
    print(sum(gear_ratios))
    # print(len(parts)548278)

    # print(sum(parts))
