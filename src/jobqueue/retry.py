from typing import Protocol


class RetryPolicy(Protocol):
    def should_retry(self, attempts: int) -> bool: ...

    def delay(self, attempts: int) -> float: ...


class NoRetry:
    def should_retry(self, attempts: int) -> bool:
        return False

    def delay(self, attempts: int) -> float:
        return 0.0


class FixedRetry:
    def __init__(self, max_attempts: int = 5, delay_in_sec: float = 1.0):
        if max_attempts <= 0:
            raise ValueError("max_attempts must be > 0")
        self._max_attempts = max_attempts
        self._delay = delay_in_sec

    def should_retry(self, attempts: int) -> bool:
        return attempts < self._max_attempts

    def delay(self, attempts: int) -> float:
        return self._delay


class ExponentialBackoff:
    def __init__(self, max_attempts: int = 5, base_delay: float = 1.0):
        if base_delay <= 0:
            raise ValueError("max_attempts must be > 0")
        self._max_attempts = max_attempts
        self._base_delay = base_delay

    def should_retry(self, attempts: int) -> bool:
        return attempts < self._max_attempts

    def delay(self, attempts: int) -> float:
        return self._base_delay * 2 ** (attempts-1)
