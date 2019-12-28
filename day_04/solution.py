import fileinput


def never_decreases(input_num: int) -> bool:
    curr_digit = None
    for digit in map(int, str(input_num)):
        if curr_digit is not None and digit < curr_digit:
            return False
        curr_digit = digit

    return True


def has_adjacent_digits_the_same(input_num: int) -> bool:
    curr_digit = None
    for digit in map(int, str(input_num)):
        if curr_digit is not None and digit == curr_digit:
            return True
        curr_digit = digit

    return False


def has_exactly_two_adjacent_digits_the_same(input_num: int) -> bool:
    curr_digit = None
    seen_count = 1
    for digit in map(int, str(input_num)):
        if curr_digit is not None and digit == curr_digit:
            seen_count += 1
        elif curr_digit is not None:
            if seen_count == 2:
                return True
            seen_count = 1
        curr_digit = digit

    if seen_count == 2:
        return True

    return False


if __name__ == "__main__":
    pass_range = list(map(int, list(fileinput.input(files=["input"]))[0].split("-")))

    # print(never_decreases(111111) and has_adjacent_digits_the_same(111111))
    # print(never_decreases(223450) and has_adjacent_digits_the_same(223450))
    # print(never_decreases(123789) and has_adjacent_digits_the_same(123789))
    # print(never_decreases(576695) and has_adjacent_digits_the_same(576695))
    # print(never_decreases(112233) and has_adjacent_digits_the_same(112233))
    # print(never_decreases(123444) and has_adjacent_digits_the_same(123444))
    # print(never_decreases(111122) and has_adjacent_digits_the_same(111122))
    #
    # print(pass_range)

    matches = []
    for i in range(pass_range[0], pass_range[1] + 1):
        if never_decreases(i) and has_adjacent_digits_the_same(i):
            matches.append(i)

    print(len(matches))

    smaller_matches = []
    for i in matches:
        if has_exactly_two_adjacent_digits_the_same(i):
            smaller_matches.append(i)

    print(len(smaller_matches))
