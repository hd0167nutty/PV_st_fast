"""/v1/samplesのpydanticスキーマ"""
from fastapi import Body
from pydantic import BaseModel, Field

class Forecasts(BaseModel):
    date:           str     = Body(description="予報日")
    weather:        str     = Body(description="天気")
    weatherURL:     str     = Body(description="天気画像URL")
    weatherDetail:  str     = Body(description="天気詳細")
    maxTemp:        int     = Body(description="最高気温")
    minTemp:        float   = Body(description="最低気温")

class AutoIn(BaseModel):
    """POST /auto の入力"""

    forecasts:      Forecasts
    rainFlag:       list[int]   = Body(description="降水フラグ")
    daylightHours:  float       = Body(description="可照時間")

class AutoOut(BaseModel):
    """POST /auto の出力"""

    result: int = Body(description="発電量")