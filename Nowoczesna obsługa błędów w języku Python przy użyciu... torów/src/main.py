def divide_by_zero(numerator: int, denominator: int) -> float:
    return numerator / denominator

def divide_by_zero_lbyl(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator != 0 else 0

def divide_by_zero_eafp(numerator: int, denominator: int) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0

if __name__ == "__main__":
    r = divide_by_zero(10, 0)
    print (f'Result: {r = }')

    r = divide_by_zero_lbyl(10, 0)
    print (f'Result: {r = }')

    r = divide_by_zero_eafp(10, 0)
    print (f'Result: {r = }')