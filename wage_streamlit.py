import numpy as np 
import pandas as pd 
import streamlit as st 
import pydeck as pdk
import plotly.express as px

st.title('日本の医療オープンデータ解析DB')
st.write('<font size="4">本DB(ダッシュボード)は厚生労働省(医療費の地域差分析)やRESASの医療系オープンデータを加工して作成しております。</font>', unsafe_allow_html=True)

option_select = st.sidebar.selectbox(
    "【①②共通】対象とする保険制度を選択して下さい",
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

disease_list = pd.read_csv('./csv_data/厚労省疾患名リスト.csv')
st.sidebar.header('【厚労省定義の疾患分類】')
st.sidebar.write(disease_list, unsafe_allow_html=True)

st.subheader('①都道府県別一人当たり医療費(円/年)(2022年)')

#disease_list.insert(0,['疾患合計'])
#r4_5.set_axis(disease_list, axis=1)

disease_list2 = r4_5.columns.values[1:]

option_disease = st.selectbox(
    '疾患分類を選択して下さい。',
    (disease_list2))

max_x = 0
#max_x = int(r4_5[option_disease].max().replace(",",""))


if option_select == '全制度計':

    if option_disease == '疾患合計':
        max_x = 500000
    else:
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
            height=800)
st.plotly_chart(fig)

st.write('<a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryouhoken/database/iryomap/index.html">出典：厚生労働省(医療費の地域差分析)(2023年12月28日公表)</a>', unsafe_allow_html=True)



st.subheader('②疾患別一人当たり医療費(円/年)(2022年)')

r4_5_t = []

if option_select == '全制度計':
    r4_5_t = pd.read_csv('./csv_data/r4-5all-t.csv')
elif option_select == '市町村国民健康保険':
    r4_5_t = pd.read_csv('./csv_data/r4-5kokuho-t.csv')
else:
    r4_5_t = pd.read_csv('./csv_data/r4-5kouki-t.csv')

#r4_5_t = r4_5_t.replace(",","")
#r4_5_t = r4_5_t.astype(int)

option_pref = st.selectbox(
    '都道府県名を選択して下さい。',
    (pref_list))

#r4_5_t[option_pref] = r4_5_t[option_pref].astype(int)

max_x2 = 0
#max_x2 = int(r4_5_t[option_pref].max())

if option_select == '全制度計':
    max_x2 = 80000
elif option_select == '市町村国民健康保険':
    max_x2 = 80000
else:
    max_x2 = 300000


fig = px.bar(r4_5_t,
            x=option_pref,
            y="疾患名",
            color="疾患名",
            range_x=[0,max_x2],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.write('<a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryouhoken/database/iryomap/index.html">出典：厚生労働省(医療費の地域差分析)(2023年12月28日公表)</a>', unsafe_allow_html=True)




st.subheader('③疾患別患者数(入院/外来(単位:千人))(2020年)')

option_inorout = st.selectbox(
    '入院 or 外来?を選択して下さい。',
    ['入院', '外来'])

if option_inorout == '入院':
    df_num_pat = pd.read_csv('./csv_data/num_inpatients.csv')
else:
    df_num_pat = pd.read_csv('./csv_data/num_outpatients.csv')

pref_list3 = df_num_pat.columns.values[1:]

option_pref3 = st.selectbox(
    '都道府県名を選択して下さい。',
    (pref_list3))

max_x3 = 0
max_x3 = int(df_num_pat[option_pref3].max())

fig = px.bar(df_num_pat,
            x=option_pref3,
            y="疾患分類",
            color="疾患分類",
            range_x=[0,max_x3],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.write('<a href="https://resas.go.jp/medical-welfare-medical-analysis/">出典：RESAS(医療・福祉マップ(医療受給))</a>', unsafe_allow_html=True)

st.subheader('④疾患別医師数/医療施設数(2020年)')
st.write('<a href="https://resas.go.jp/medical-welfare-medical-analysis/">出典：RESAS(医療・福祉マップ(医療受給))</a>', unsafe_allow_html=True)



