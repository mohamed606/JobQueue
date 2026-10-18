import pytest

from jobqueue.job import JobStatus, Job


def add(x, y):
    return x + y


def always_fail():
    raise ValueError('Always fail')


def test_execute_pass_kwargs():
    job = Job(func=add, kwargs={'x': 10, 'y': 20})
    job_result = job.execute()
    assert job_result == 30


def test_execute_pass_args():
    job = Job(func=add, args=(10, 20))
    job_result = job.execute()
    assert job_result == 30


def test_execute_pass_kwargs_and_args():
    job = Job(func=add, args=(10,), kwargs={'y': 20})
    job_result = job.execute()
    assert job_result == 30


def test_execute_increments_attempts():
    job = Job(func=add, args=(10, 20))
    job.execute()
    job.execute()
    assert job.attempts == 2


def test_execute_reraises_function_error():
    job = Job(func=always_fail)
    with pytest.raises(ValueError):
        job.execute()


def test_attempts_count_even_when_function_fails():
    job = Job(func=always_fail)
    with pytest.raises(ValueError):
        job.execute()
    assert job.attempts == 1


def test_new_job_defaults():
    job = Job(func=add, args=(10, 20))
    assert job.attempts == 0
    assert job.status.value == JobStatus.PENDING.value


def test_each_job_get_unique_id():
    ids = set()
    for _ in range(10):
        ids.add(Job(func=add, args=(10, 20)).id)
    assert len(ids) == 10


def test_does_not_change_status():
    job = Job(func=add, args=(10, 20))
    job.execute()
    assert job.status == JobStatus.PENDING
