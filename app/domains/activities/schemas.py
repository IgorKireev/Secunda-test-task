from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator

MAX_DEPTH = 3


class ActivityBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    children: list[ActivityBase] = Field(default_factory=list)
    _depth: int = Field(default=0, repr=False, exclude=True)


    @classmethod
    @model_validator(mode='after')
    def validate_children(cls, model):
        if model._depth >= MAX_DEPTH:
            raise ValueError(f"Максимальная глубина активности ({MAX_DEPTH}) превышена")

        titles = [child.title for child in model.children]
        if len(titles) != len(set(titles)):
            raise ValueError("Дублирующиеся названия на одном уровне недопустимы")

        for child in model.children:
            child._depth = model._depth + 1

        return model

    class Config:
        from_attributes = True


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    parent_id: int | None = None

    class Config:
        from_attributes = True