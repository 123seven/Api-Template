from fastapi import FastAPI, Request

import redis
from redis import ConnectionPool

from app.core.config import settings


def init_redis(app: FastAPI, add_exception_handlers: bool = False) -> None:
    """
    redis pool initialized
    """

    def get_redis_pool() -> redis.ConnectionPool:
        return ConnectionPool(
            host=settings.REDIS_DSN.host, port=settings.REDIS_DSN.port,
            encoding="utf-8", decode_responses=True
        )

    @app.on_event("startup")
    async def startup_redis_event():
        app.state.redis_pool = get_redis_pool()

    @app.on_event("shutdown")
    async def shutdown_redis_event():
        if app.state.redis_pool:
            await app.state.redis_pool.disconnect()

    if add_exception_handlers:
        pass


def get_redis(request: Request):
    redis_client = redis.Redis(
        connection_pool=request.app.state.redis_pool,
    )
    try:
        yield redis_client
    finally:
        redis_client.close()
