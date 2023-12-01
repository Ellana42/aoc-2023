import argparse

import regex

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get digits",
    )
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        input_ = f.readlines()

    digit_words = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    digits = [
        regex.findall(r"\d|" + "|".join(digit_words), line, overlapped=True)
        for line in input_
    ]
    digits = [
        [
            digit_words.index(digit) + 1 if digit in digit_words else int(digit)
            for digit in line
        ]
        for line in digits
    ]
    numbers = [digits[0] * 10 + digits[-1] for digits in digits]
    result = sum(numbers)
    print(f"Result {result}")
