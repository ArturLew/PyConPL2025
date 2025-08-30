from returns.result import safe
from returns.pipeline import is_successful

@safe
def divide_by_zero(numerator: int, denominator: int) -> float:
    return numerator / denominator

@safe(exceptions=(ZeroDivisionError,))
def divide_by_zero_expl(numerator: int, denominator: int) -> float:
    return numerator / denominator

if __name__ == "__main__":
    r = divide_by_zero(10, 0)

    print (f'Result: {r = }')
    if is_successful(r):
        print(f'Success: {r.unwrap()}')
    else:
        print(f'Failure: {r.failure()}')

    r = divide_by_zero_expl(10, 0)

    print (f'Result: {r = }')
    if is_successful(r):
        print(f'Success: {r.unwrap()}')
    else:
        print(f'Failure: {r.failure()}')