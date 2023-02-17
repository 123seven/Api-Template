from pydantic import BaseModel, Field

__all__ = [
    "PaginatorBySchema",
]


class PaginatorBySchema(BaseModel):
    page: int = Field(default=1, ge=0)
    page_size: int = Field(default=20, ge=0, le=100)
