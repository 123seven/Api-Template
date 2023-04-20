from fastapi import APIRouter, BackgroundTasks, Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.api.service.example import ExampleServices
from app.core.cbv import cbv
from app.core.response import ResponseModel
from app.models.database import get_session
from app.tools.redis_client import get_redis

router = APIRouter()


@cbv(router)
class ExampleViewApi:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session),
        redis: Redis = Depends(get_redis),
    ):
        self.service = ExampleServices(session, redis, background_tasks)

    @router.get("/hello", response_model=ResponseModel)
    async def hello(self):
        return await self.service.hello()
