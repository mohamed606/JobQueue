import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class JobStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'


@dataclass
class Job:
    func: Callable[..., Any]
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    attempts: int = 0
    result: Any = None
    error: str | None = None

    def execute(self)-> Any:
        self.attempts += 1
        return self.func(*self.args, **self.kwargs)
