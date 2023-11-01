"""/v1/samplesのpydanticスキーマ"""
from fastapi import Query
from pydantic import BaseModel, Field

class ManualIn(BaseModel):
    """GET /manual の入力"""

    m:      int = Field(Query(description="月"))
    d:      int = Field(Query(description="日"))
    max:    int = Field(Query(description="最高気温"))
    min:    int = Field(Query(description="最低気温"))
    amt:    float = Field(Query(description="日射量"))


class ManualOut(BaseModel):
    """GET /manual の出力"""

    result: int = Field(description="発電量")