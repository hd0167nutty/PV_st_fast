import numpy as np
import datetime
import pickle
import pandas as pd
from .my_function import generated_power_amount


def _load_model():
    with open('./backend/models/model_solar_radiation_main.pkl', 'rb') as f:    
        return pickle.load(f)

def _edit_input_data(query, date):
    input_data = []
    # date = datetime.datetime.strptime(query.forecasts.date,'%Y-%m-%d')
    input_data.append(int(date.month))              # 予報日付(月)
    input_data.append(int(date.day))                # 予報日付(日)
    input_data.append(int(query.forecasts.maxTemp)) # 最高気温
    input_data.append(int(query.forecasts.minTemp)) # 最低気温
    input_data.append(query.daylightHours)          # 可照時間
    input_data.append(0 if int(query.forecasts.maxTemp)<25 else 1)  # 夏日フラグ
    input_data.append(int(query.rainFlag[2]))    # 9時降水フラグ
    input_data.append(int(query.rainFlag[3]))    # 12時降水フラグ
    input_data.append(int(query.rainFlag[4]))    # 15時降水フラグ
    input_data.append(int(query.rainFlag[5]))    # 18時降水フラグ
    return input_data

def get_power_generations(query) -> int:
    # モデル読込
    model = _load_model()
    date = datetime.datetime.strptime(query.forecasts.date,'%Y-%m-%d')
    # 目的変数
    x = _edit_input_data(query, date)
    x = np.array(x).reshape(1,-1)

    # 推論(斜面日射量)
    pred = model.predict(x)
    # 演算(太陽光発電設備に応じた発電量算出)
    result = generated_power_amount(pred[0], int(date.month))
     
    return result
