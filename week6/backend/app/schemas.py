from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1, max_length=2000)


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True


class BulkCompleteRequest(BaseModel):
    ids: list[int] = Field(min_length=1)


class Paginated(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class ExtractResult(BaseModel):
    hashtags: list[str]
    action_items: list[str]
    applied: bool = False
    created_action_item_ids: list[int] = Field(default_factory=list)


SortOption = Literal["created_desc", "title_asc"]
