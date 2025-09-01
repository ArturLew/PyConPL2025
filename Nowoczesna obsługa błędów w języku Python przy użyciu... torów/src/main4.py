from returns.result import safe, Success, Failure

@safe
def divide_by_zero(numerator: int, denominator: int) -> float:
    return numerator / denominator

if __name__ == "__main__":
    r = divide_by_zero(10, 0)

    match r:
        case Success(item):
            print(f"Success: {item}")
        case Failure(error):
            print(f"Failure: {error}")
        case Failure(ZeroDivisionError()):
            print('"ZeroDivisionError" was raised')
        case Failure(_):
            print('The division was a failure')