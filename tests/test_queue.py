import pytest

from jobqueue.job import Job
from jobqueue.queue import InMemoryQueue


def noob():...

def make_job():
    return Job(func=noob)

@pytest.fixture
def empty_queue():
    return InMemoryQueue()

@pytest.fixture
def queue_with_jobs():
    queue = InMemoryQueue()
    for i in range(10):
        queue.enqueue(make_job())
    return queue

def test_dequeue_from_empty_queue(empty_queue):
    job = empty_queue.dequeue()
    assert job is None


def test_dequeue_returns_jobs_in_fifo_order():
    queue = InMemoryQueue()
    job1, job2, job3 = make_job(), make_job(), make_job()
    queue.enqueue(job1)
    queue.enqueue(job2)
    queue.enqueue(job3)

    assert queue.dequeue() is job1
    assert queue.dequeue() is job2
    assert queue.dequeue() is job3


def test_dequeue_from_queue_until_empty(queue_with_jobs):
    length_of_queue = len(queue_with_jobs)
    for i in range(length_of_queue):
        queue_with_jobs.dequeue()

    assert queue_with_jobs.dequeue() is None


def test_len_of_queue_when_adding_jobs(queue_with_jobs):
    assert len(queue_with_jobs) == 10


def test_len_of_queue_when_empty(empty_queue):
    assert len(empty_queue) == 0

def test_len_decreases_after_dequeue(queue_with_jobs):
    job = queue_with_jobs.dequeue()
    assert len(queue_with_jobs) == 9