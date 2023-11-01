import pickle
import pandas as pd
from .my_function import generated_power_amount


def _load_model():
    with open('./backend/models/model_solar_radiation_input.pkl', 'rb') as f:    
        return pickle.load(f)

def get_power_generations(query) -> int:
    # モデル読込
    model = _load_model()
    # Input Data(1 row DataFrame)
    value_df = pd.DataFrame([], columns=['月','日', '最高気温','最低気温', '水平面全天日射量'])
    record = pd.Series([query.m, query.d, query.max, query.min, query.amt ], index=value_df.columns)
    value_df = pd.concat([value_df, pd.DataFrame([record])], ignore_index=True, axis=0)

    x = value_df.copy()
    # 推論(斜面日射量)
    pred = model.predict(x)
    # 演算(太陽光発電設備に応じた発電量算出)
    result = generated_power_amount(pred[0], query.m)
     
    return result
