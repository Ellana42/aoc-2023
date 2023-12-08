import argparse


def get_input(filename):
    with open(filename) as f:
        input_ = f.read()

    input_lines = input_.split("\n\n")
    return [line.strip("\n") for line in input_lines]


def get_seeds(header: str):
    return [int(seed) for seed in header.split(" ")[1:]]


def parse_maps(input_maps):
    maps = []
    for map in input_maps:
        map_lines = map.split("\n")
        values = [
            tuple(int(val) for val in mapping.split(" ")) for mapping in map_lines[1:]
        ]
        maps.append(values)
    return maps


def apply_mapping(x, destination, source, length):
    if source <= x < source + length:
        return x - source + destination
    return x


def compute_location(seed: int, maps):
    for category in maps:
        for destination, source, length in category:
            previous_seed = seed
            seed = apply_mapping(seed, destination, source, length)
            if seed != previous_seed:
                break
    return seed


def test_example():
    input_ = get_input("example")
    seeds = get_seeds(input_[0])
    maps = parse_maps(input_[1:])
    locations = {seed: compute_location(seed, maps) for seed in seeds}
    assert locations[79] == 82
    assert locations[14] == 43
    assert locations[55] == 86
    assert locations[13] == 35


def get_min_locations(filename):
    input_ = get_input(filename)
    seeds = get_seeds(input_[0])
    maps = parse_maps(input_[1:])
    locations = [compute_location(seed, maps) for seed in seeds]
    return min(locations)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get digits",
    )
    parser.add_argument("input_file")
    args = parser.parse_args()

    print(get_min_locations(args.input_file))
