import pytest

from jobqueue.retry import NoRetry, FixedRetry, ExponentialBackoff


@pytest.fixture
def no_retry_policy():
    return NoRetry()


@pytest.fixture
def fixed_retry_policy():
    return FixedRetry(4, 1.0)

@pytest.fixture
def exponential_backoff_retry_policy():
    return ExponentialBackoff(4, 1.0)


def test_no_retry_policy(no_retry_policy):
    assert no_retry_policy.should_retry(5) == False


def test_no_retry_policy_delay(no_retry_policy):
    assert no_retry_policy.delay(6) == 0.0


def test_fixed_retry_policy_should_retry_after_first_attempt(fixed_retry_policy):
    assert fixed_retry_policy.should_retry(1) == True


def test_fixed_retry_policy_should_not_retry_after_reaching_max_attempts(fixed_retry_policy):
    assert fixed_retry_policy.should_retry(4) == False


def test_fixed_retry_policy_delay(fixed_retry_policy):
    assert fixed_retry_policy.delay(2) == 1.0


def test_exponential_backoff_should_retry_while_not_reaching_max_attempts(exponential_backoff_retry_policy):
    assert exponential_backoff_retry_policy.should_retry(2) == True

@pytest.mark.parametrize(
    "attempts, expected_delay",
    [
        (1, 1.0),
        (2, 2.0),
        (3, 4.0),
        (4, 8.0),
    ]
)
def test_exponential_backoff_delay(attempts, expected_delay):
    policy = ExponentialBackoff(max_attempts=5, base_delay=1.0)
    assert policy.delay(attempts) == expected_delay


@pytest.mark.parametrize(
    "attempts, expected",
    [
        (1, True),
        (3, True),
        (4, False),
        (5, False),
    ],
)
def test_fixed_retry_should_retry(attempts, expected):
    policy = FixedRetry(max_attempts=4, delay_in_sec=1.0)
    assert policy.should_retry(attempts) is expected