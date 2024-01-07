import numpy as np 
import pandas as pd 
import streamlit as st 
import pydeck as pdk
import plotly.express as px

st.title('日本の医療オープンデータ解析DB')
st.text('本結果は厚生労働省(医療費の地域差分析)やRESASの医療系オープンデータを加工して作成しております。')

option_select = st.sidebar.selectbox(
    "対象とする保険制度を選択して下さい",
    ('市町村国民健康保険','後期高齢者医療制度','全制度計')
)
st.sidebar.write(option_select,'を選択中')

r4_5 = []

if option_select == '全制度計':
    r4_5 = pd.read_csv('./csv_data/r4-5all.csv')
elif option_select == '市町村国民健康保険':
    r4_5 = pd.read_csv('./csv_data/r4-5kokuho.csv')
else:
    r4_5 = pd.read_csv('./csv_data/r4-5kouki.csv')

pref_list = r4_5["都道府県名"]

disease_list =pd.read_csv('./csv_data/厚労省疾患名リスト.csv')
st.sidebar.header('【厚労省定義の疾患分類】')
st.sidebar.text(disease_list)

st.header('■都道府県別一人当たり医療費(万円/年)(2022年)')

disease_list2 = r4_5.columns.values[1:]

option_disease = st.selectbox(
    '疾患名',
    (disease_list2))

max_x = 0

if option_select == '全制度計':

    if option_disease == '疾患合計':
        max_x = 500000
    else:
        #max_x = r4_5_all[option_disease].max().astype(int)
        max_x = 80000

elif option_select == '市町村国民健康保険':

        if option_disease == '疾患合計':
            max_x = 500000
        else:
            max_x = 80000

else:
         if option_disease == '疾患合計':
            max_x = 1200000
         else:
            max_x = 300000

   

fig = px.bar(r4_5,
            x=option_disease,
            y="都道府県名",
            color="都道府県名",
            range_x=[0,max_x],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.text('出典：厚生労働省(医療費の地域差分析)')



st.header('■疾患別一人当たり医療費(万円/年)(2022年)')

r4_5_t = []

if option_select == '全制度計':
    r4_5_t = pd.read_csv('./csv_data/r4-5all-t.csv')
elif option_select == '市町村国民健康保険':
    r4_5_t = pd.read_csv('./csv_data/r4-5kokuho-t.csv')
else:
    r4_5_t = pd.read_csv('./csv_data/r4-5kouki-t.csv')

option_pref = st.selectbox(
    '都道府県名',
    (pref_list))

max_x = 0

if option_select == '全制度計':
    max_x = 80000
elif option_select == '市町村国民健康保険':
    max_x = 80000
else:
    max_x = 300000

fig = px.bar(r4_5_t,
            x=option_pref,
            y="疾患名",
            color="疾患名",
            range_x=[0,max_x],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.text('出典：厚生労働省(医療費の地域差分析)')


