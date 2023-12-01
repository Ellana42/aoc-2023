import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get digits",
    )
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file) as f:
        input_ = f.read()
    lines = [line for line in input_.split("\n")][:-1]
    digits = [[c for c in line if c.isdigit()] for line in lines]
    numbers = [int(digits[0] + digits[-1]) for digits in digits]
    result = sum(numbers)
    print(f"Result {result}")
