"""Task 1: Fibonacci numbers with a cache kept in a closure."""

from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """Return a `fibonacci(n)` function that remembers computed values."""
    # The cache lives in the enclosing scope, so it is shared between calls.
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        """Return the n-th Fibonacci number (0 for n <= 0)."""
        if n <= 0:
            return 0
        if n == 1:
            return 1
        # Reuse an already computed value.
        if n in cache:
            return cache[n]
        # Compute recursively and store the result for later calls.
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # 55
    print(fib(15))  # 610
