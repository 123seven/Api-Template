from fastapi import APIRouter, Query, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from redis import Redis
from sqlmodel import Session

from app.api.service.chat import ChatServices
from app.core.cbv import cbv
from app.core.response import ResponseModel
from app.models.database import get_session
from app.tools.redis_client import get_redis

router = APIRouter()


@cbv(router)
class ChatGPTViewApi:

    def __init__(
            self,
            background_tasks: BackgroundTasks,
            session: Session = Depends(get_session),
            redis: Redis = Depends(get_redis),
    ):
        self.service = ChatServices(session, redis, background_tasks)

    @router.get("/ask", response_model=ResponseModel)
    async def ask(self, message: str = Query(None, description=""), ):
        result = await self.service.ask(message)
        return result

    @router.get("/ask/stream", response_model=ResponseModel)
    def ask_stream(self, message: str = Query(None, description=""), ):
        return StreamingResponse(
            self.service.ask_stream(message),
            media_type="text/plain",
        )
