from sqlmodel import SQLModel


class DefaultRequestParam(SQLModel):
    limit: int | None = None
    offset: int | None = 0
