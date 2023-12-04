import argparse
from enum import Enum
from functools import reduce
import operator
from typing import Dict, List


class Color(Enum):
    red = "red"
    blue = "blue"
    green = "green"


def get_game_index(game_report: str) -> int:
    game = game_report.split(":")[0]
    index = game.split(" ")[1]
    return int(index)


def reveal_sequence_to_rgb(reveal_sequence: str) -> Dict[Color, int]:
    ball_reports = reveal_sequence.strip(" ").split(", ")
    return {
        Color(ball_report.split(" ")[1]): int(ball_report.split(" ")[0])
        for ball_report in ball_reports
    }


def get_ball_repartition(game_report: str) -> Dict[Color, List[int]]:
    balls_revealed = game_report.strip("\n").split(":")[1]
    reveal_sequences = balls_revealed.split(";")
    reveal_sequences = [
        reveal_sequence_to_rgb(reveal_sequence) for reveal_sequence in reveal_sequences
    ]
    return {
        color: [
            reveal_sequence[color]
            for reveal_sequence in reveal_sequences
            if color in reveal_sequence
        ]
        for color in Color
    }


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="get digits",
    )
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        input_ = f.readlines()

    bag_repartition = {
        Color.blue: 14,
        Color.red: 12,
        Color.green: 13,
    }
    games = [line.split(":") for line in input_]
    games = {get_game_index(line): get_ball_repartition(line) for line in input_}
    max_games = {
        index: {color: max(draw) for color, draw in draws.items()}
        for index, draws in games.items()
    }
    set_power = [reduce(operator.mul, game.values()) for game in max_games.values()]
    print(set_power)
    print(sum(set_power))
