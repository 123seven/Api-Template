from fastapi import BackgroundTasks
from redis import Redis
from sqlmodel import Session

from app.core.response import SuccessResult


class ExampleServices:
    def __init__(
        self, session: Session, redis: Redis, background_tasks: BackgroundTasks
    ):
        self.session = session
        self.redis = redis
        self.tasks = background_tasks

    @classmethod
    async def hello(cls):
        return SuccessResult(data={"reply": "Hi FastAPI"})
