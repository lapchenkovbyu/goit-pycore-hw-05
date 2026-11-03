"""Task 2: sum of the real numbers found in a text."""

import re
from typing import Callable, Iterator


def generator_numbers(text: str) -> Iterator[float]:
    """Yield every real number in `text` as a float.

    A number must have whitespace on both sides, e.g. ' 27.45 '.
    """
    # Lookarounds require spaces around the number without consuming them.
    pattern = r"(?<=\s)\d+\.\d+(?=\s)"
    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """Return the sum of the numbers produced by `func(text)`."""
    # round() removes floating point noise such as 1351.4600000000002.
    return round(sum(func(text)), 2)


if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
