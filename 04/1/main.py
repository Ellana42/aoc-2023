import argparse
import re


def get_cards(input_):
    cards = {}
    for line in input_:
        result = re.search(r"^Card[ ]+(\d+): ([\d ]+) \| ([\d ]+)$", line)
        if result is None:
            print(line)
            print("problem with regex")
            continue
        card_index, winning_nbs, my_nbs = result.groups()
        winning_nbs = set(
            int(nb) for nb in winning_nbs.split(" ") if len(nb.strip()) > 0
        )
        my_nbs = [int(nb) for nb in my_nbs.split(" ") if len(nb.strip()) > 0]
        cards[int(card_index)] = (winning_nbs, my_nbs)
    return cards


def get_scores(cards):
    return [
        len([nb for nb in my_nbs if nb in winning_nbs])
        for winning_nbs, my_nbs in cards.values()
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        input_ = f.readlines()

    cards = get_cards(input_)
    scores = get_scores(cards)
    scores = [2 ** (score - 1) if score > 0 else 0 for score in scores]
    print(scores)
    print(len(scores))
    print(sum(scores))
