# -*- coding: utf-8 -*-
from datetime import datetime
import requests
import streamlit as st
import os
import json

# FastAPIのエンドポイント
# Streamlit Share の環境変数へ Render のデプロイURLを設定する
# 環境変数に RENDER_URL が設定されていない場合はデフォルトのURLを設定する
url = os.environ.get("RENDER_URL") or 'http://localhost:8000'
        
def load_json_file():
    url = 'https://raw.githubusercontent.com/hd0167nutty/scrap_weather_info/main/forecasts.json'
    data = requests.get(url)
    json_data = json.loads(data.text)
    return json_data    
        
def main():
    # 事前にスクレイピングしていた天気予報jsonを取得
    json_data = load_json_file()
    # JSON形式の文字列をPOSTする
    response = requests.post(f"{url}/auto/", json= json_data)
    
    forecasts = json_data['forecasts']          # 天気予報（明日）
    # date = forecasts["date"]                    # 日付
    date = datetime.strptime(forecasts["date"],'%Y-%m-%d')  # 日付
    weather = forecasts["weather"]              # 天気
    weatherURL = forecasts["weatherURL"]        # 天気画像
    weatherDetail = forecasts["weatherDetail"]  # 天気詳細
    maxTemp = forecasts["maxTemp"]              # 最高気温
    minTemp = forecasts["minTemp"]              # 最高気温

    st.title("明日の発電量予測🌦️")
    st.header('{0:%Y年%m月%d日}'.format(date))
    st.image(weatherURL)
    st.write(weather)
    st.write(f'天気詳細: {weatherDetail}')
    st.markdown(f'最高気温: :red[{maxTemp} ℃]')
    st.markdown(f'最低気温: :blue[{minTemp} ℃]')

    if response.status_code == 200:
        result = response.json()['result']
        # st.json(json_data)
        # st.write(result)
        st.markdown(f'### 明日の発電量はきっと <span style="font-family:monospace; color:purple; font-size: 35px;">{result}</span> kWh', unsafe_allow_html=True)

    else:
        st.error(f'{response.status_code}エラーが発生しました')
        st.json(response.json())

if __name__ == '__main__':
    main()
