import math

import pandas as pd

from decimal import Decimal, ROUND_HALF_UP  # class RoundUtilに必要ライブラリー
# 一般的な四捨五入をする
class RoundUtil:
    def round(value, digit = 0):
        exp = '0' if digit == 0 else '0.' + ''.join(['0' for x in range(digit)])
        return Decimal(str(value)).quantize(Decimal(exp), rounding=ROUND_HALF_UP)

def generated_power_amount(H_MJ, month):
    _ = """
    1日の発電量を算出
    E_pd = K * P_as * H_kWh
    H_kWh = H_MJ * 0.278
    K = _K * K_pt
    _K = KHD * KPD * KPA * KPM * hINO
    K_pt = 1 + 0.01 * a_pmax * (T_cr - 25)
    a_pmax = -0.43
    K_pt は月別にcsvファイルに格納
    H_MJ: 斜面日射量(MJ/m2)
    H_kWh: 斜面日射量(kWh/m2)
    """
    df_K = pd.read_csv('./frontend/data/基本設計係数.csv', header=None)
    df_Kpt = pd.read_csv('./frontend/data/月別温度補正係数.csv')

    # 予報日付の月から月別温度補正係数を格納
    K_pt = df_Kpt['KPT'][df_Kpt['month']==(str(month) + '月')].iloc[-1]
    K_pt = Decimal(str(K_pt))
    _K = math.prod(df_K.iloc[:5,2])         # 基本設計係数の乗算
    _K = Decimal(str(_K))
    P_as = Decimal('49.5')                  # アレイ出力
    coeff_MJ_to_kWh = Decimal('3.6')        # MJをkWhに単位変換する係数

    K = _K * K_pt
    H_kWh = Decimal(str(H_MJ)) / coeff_MJ_to_kWh # 単位変換
    E_pd = K * P_as * H_kWh

    return RoundUtil.round(E_pd)

