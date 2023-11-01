# Library
import streamlit as st
import requests
import pandas as pd
import datetime
import os

# FastAPIのエンドポイント
# Streamlit Share の環境変数へ Render のデプロイURLを設定する
# 環境変数に RENDER_URL が設定されていない場合はデフォルトのURLを設定する
url = os.environ.get("RENDER_URL") or 'http://localhost:8000'

with st.sidebar.form("Form1"):
    # Sidebar(Input)
    date = (datetime.datetime.now() + datetime.timedelta(days=1))
    tomorrowValue = date.strftime('%Y-%m-%d')
    st.write(tomorrowValue)
    maxTemp = st.slider('最高気温(度)', min_value=0.0, max_value=40.0, step=1.0, value=20.0)
    minTemp = st.slider('最低気温(度)', min_value=-10.0, max_value=30.0, step=1.0, value=10.0)
    amount = st.slider('日射量(MJ/m2)', min_value=0.0, max_value=30.0, step=0.5, value=10.0)

    submitted = st.form_submit_button("予測する")
    
# Main Panel
st.title('明日の発電量予測(kWh)')

if submitted:
    response = requests.get(f"{url}/manual/", params={"m": date.month, "d": date.day, "max": maxTemp, "min": minTemp, "amt": amount})
    if response.status_code == 200:
        result = response.json()['result']
        st.write('### 説明変数')

        # Input Data(1 row DataFrame)
        value_df = pd.DataFrame([], columns=['月','日', '最高気温','最低気温', '水平面全天日射量'])
        record = pd.Series([date.month, date.day, maxTemp, minTemp, amount ], index=value_df.columns)
        value_df = pd.concat([value_df, pd.DataFrame([record])], ignore_index=True, axis=0)

        # Input value
        st.write(value_df)
        
        # st.success(f'**{result}**kWh',icon='🌞')
        st.markdown(f'### 明日の発電量はきっと <span style="font-family:monospace; color:purple; font-size: 35px;">{result}</span> kWh', unsafe_allow_html=True)

    else:
        st.error(f'{response.status_code}エラーが発生しました')
        st.json(response.json())

# st.latex(r''' \frac{n!}{k!(n-k)!} = \binom{n}{k} ''')



