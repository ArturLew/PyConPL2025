import pyperf

from returns.result import safe

def divide_by_zero_traditional(numerator: int, denominator: int) -> float:
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0

@safe
def divide_by_zero_returns(numerator: int, denominator: int) -> float:
    return numerator / denominator

def test_divide_by_zero_traditional_no_error():
    return divide_by_zero_traditional(10, 1)

def test_divide_by_zero_traditional_with_error():
    return divide_by_zero_traditional(10, 0)

def test_divide_by_zero_returns_no_error():
    return divide_by_zero_returns(10, 1)

def test_divide_by_zero_returns_with_error():
    return divide_by_zero_returns(10, 0)

if __name__ == "__main__":
    runner = pyperf.Runner(processes=1, values=20, warmups=2, min_time=0.02,)
    runner.bench_func("divide_by_zero_traditional no error", test_divide_by_zero_traditional_no_error)
    runner.bench_func("divide_by_zero_returns no error", test_divide_by_zero_returns_no_error)

    runner.bench_func("divide_by_zero_traditional with error", test_divide_by_zero_traditional_with_error)
    runner.bench_func("divide_by_zero_returns with error", test_divide_by_zero_returns_with_error)