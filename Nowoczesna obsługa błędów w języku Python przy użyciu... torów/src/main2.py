from returns.result import Success, Failure
from returns.pipeline import is_successful

def divide_by_zero_lbyl(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return Failure('Division by zero')
    return Success(numerator / denominator)

def divide_by_zero_eafp(numerator: int, denominator: int) -> float:
    try:
        return Success(numerator / denominator)
    except ZeroDivisionError as ex:
        return Failure(ex)

if __name__ == "__main__":
    r = divide_by_zero_lbyl(10, 0)
    print (f'Result: {r = }')
    
    if is_successful(r):
        print(f'Success: {r.unwrap()}')
    else:
        print(f'Failure: {r.failure()}')

    r = divide_by_zero_eafp(10, 0)
    print (f'Result: {r = }')
    if is_successful(r):
        print(f'Success: {r.unwrap()}')
    else:
        print(f'Failure: {r.failure()}')
