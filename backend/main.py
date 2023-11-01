from fastapi import FastAPI, Depends
from .libs import auto_solar, manual_solar
from .schemas import autos, manuals

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/auto/", response_model=autos.AutoOut)
async def predict_auto(query: autos.AutoIn):
    """天気予報から明日の太陽光発電量予測"""
    return {'result':auto_solar.get_power_generations(query)}
    # return {'result': query.forecasts.minTemp}

@app.get("/manual/", response_model=manuals.ManualOut)
async def predict_manual(query: manuals.ManualIn = Depends()):
    """入力値から明日の太陽光発電量予測"""
    return {'result':manual_solar.get_power_generations(query)}
    # return {'result': query.amt}
