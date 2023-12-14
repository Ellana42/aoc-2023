from __future__ import annotations
import argparse
from typing import List, Tuple

# def get_inflexion_points_mapping(source, length):
#     return source, source + length + 1


# def get_seeds_final_inflexion_points(maps):
#     seeds = []
#     for destination, source, length in maps[-1]:
#         inflexion_points = get_inflexion_points_mapping(source, length)
#         for inflexion_point in inflexion_points:
#             seeds.append(reverse_engineer_location(inflexion_point, maps))
#     return seeds


# def reverse_mapping(x, destination, source, length):
#     presumed_reversal = x + source - destination
#     if source <= presumed_reversal < source + length:
#         return presumed_reversal
#     return x


# def reverse_engineer_location(location, maps):
#     for category in reversed(maps):
#         for destination, source, length in category:
#             previous_location = location
#             location = reverse_mapping(location, destination, source, length)
#             if location != previous_location:
#                 break
#     return location


class Range:
    def __init__(self, start, end) -> None:
        if start > end:
            raise ValueError
        self.start: int = start
        self.end: int = end  # included

    def contains(self, value: int):
        return self.start <= value <= self.end

    def contains_range(self, range_: "Range"):
        return self.contains(range_.start) and self.contains(range_.end)

    def overlaps(self, range_: "Range"):
        return (
            self.contains(range_.start)
            or self.contains(range_.end)
            or range_.contains_range(self)
            or self.contains_range(range_)
        )

    def overlaps_left(self, range_: "Range"):
        return self.contains(range_.start)

    def overlaps_right(self, range_: "Range"):
        return self.contains(range_.end)

    def is_after(self, value: int):
        return value < self.start

    def is_before(self, value: int):
        return value > self.end

    def split(self, values: List[int]) -> List[Range]:
        result = []
        end_last_split = self.start - 1
        for value in sorted(values):
            if self.contains(value - 1):
                result.append(Range(end_last_split + 1, value - 1))
                end_last_split = value - 1
        result.append(Range(end_last_split + 1, self.end))
        return result

    def transform(self, value: int):
        self.start += value
        self.end += value
        return self

    def __repr__(self) -> str:
        return f"[{self.start} -> {self.end}]"


class Mapping:
    def __init__(self, destination, source, lenght) -> None:
        self.destination = destination
        self.source = source
        self.lenght = lenght
        self.destination_range: Range = Range(destination, destination + lenght - 1)
        self.source_range: Range = Range(source, source + lenght - 1)
        self.value = self.destination_range.start - self.source_range.start

    def apply(self, value: int):
        if self.source_range.contains(value):
            return value + self.value
        return value

    def apply_range(self, range_: Range):
        if not range_.overlaps(self.source_range):
            return [(range_, False)]
        split_range = range_.split([self.source_range.start, self.source_range.end])
        split_range = [
            (subrange.transform(self.value), True)
            if subrange.overlaps(self.source_range)
            else (subrange, False)
            for subrange in split_range
        ]
        return split_range

    def __repr__(self) -> str:
        return f"{self.source_range} ==> {self.destination_range} ({'+' if self.destination >= self.source else ''}{self.destination - self.source})"


class Map:
    def __init__(self, destination, source, lenght) -> None:
        self.destination = destination
        self.source = source
        self.lenght = lenght
        self.destination_range: Range = Range(destination, destination + lenght - 1)
        self.source_range: Range = Range(source, source + lenght - 1)
        self.value = self.destination_range.start - self.source_range.start

    def apply(self, value: int):
        if self.source_range.contains(value):
            return value + self.value
        return value

    def apply_range(self, range_: Range):
        if not range_.overlaps(self.source_range):
            return [(range_, False)]
        split_range = range_.split([self.source_range.start, self.source_range.end])
        split_range = [
            (subrange.transform(self.value), True)
            if subrange.overlaps(self.source_range)
            else (subrange, False)
            for subrange in split_range
        ]
        return split_range

    def __repr__(self) -> str:
        return f"{self.source_range} ==> {self.destination_range} ({'+' if self.destination >= self.source else ''}{self.destination - self.source})"


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def get_input(filename):
    with open(filename) as f:
        input_ = f.read()

    input_lines = input_.split("\n\n")
    return [line.strip("\n") for line in input_lines]


def get_seed_ranges(header: str):
    seed_ranges = [int(seed) for seed in header.split(" ")[1:]]
    seeds = []
    for start, length in pairwise(seed_ranges):
        seeds.append((start, start + length - 1))
    return seeds


def map_range(mapping, input_ranges):
    output_ranges = []
    for destination, source, lenght in mapping:
        new_input_ranges = []
        for start_range, end_range in input_ranges:
            constant_ranges, modified_range = transform_range(
                destination, source, lenght, start_range, end_range
            )
            new_input_ranges.extend(constant_ranges)
            if modified_range is not None:
                output_ranges.append(modified_range)
        input_ranges = new_input_ranges
    output_ranges.extend(constant_ranges)
    return output_ranges


def get_range_location(mappings, input_ranges):
    for mapping in mappings:
        input_ranges = map_range(mapping, input_ranges)
    return input_ranges


def parse_maps(input_maps):
    maps = []
    for map in input_maps:
        map_lines = map.split("\n")
        values = [
            tuple(int(val) for val in mapping.split(" ")) for mapping in map_lines[1:]
        ]
        maps.append(values)
    return maps


def compute_location(seed: int, maps):
    for category in maps:
        for destination, source, length in category:
            previous_seed = seed
            seed = apply_mapping(seed, destination, source, length)
            if seed != previous_seed:
                break
    return seed


def test_example():
    assert get_min_locations("example") == 46


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

    # print(get_min_loh = fications(args.input_file))
