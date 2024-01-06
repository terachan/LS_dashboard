import numpy as np 
import pandas as pd 
import streamlit as st 
import pydeck as pdk
import plotly.express as px

st.title('日本の医療オープンデータ解析DB')
st.text('本結果は厚生労働省(医療費の地域差分析)のオープンデータを加工して作成しております。')

df_jp_ind = pd.read_csv('./csv_data/雇用_医療福祉_一人当たり賃金_全国_全産業.csv',encoding = 'shift_jis')
df_jp_category = pd.read_csv('./csv_data/雇用_医療福祉_一人当たり賃金_全国_大分類.csv',encoding = 'shift_jis')
df_pref_ind = pd.read_csv('./csv_data/雇用_医療福祉_一人当たり賃金_都道府県_全産業.csv',encoding = 'shift_jis')

r4_5_all = []
r4_5_all = pd.read_csv('./csv_data/r4-5all.csv')

disease_list =pd.read_csv('./csv_data/厚労省疾患名リスト.csv')
st.sidebar.header('【厚労省定義の疾患分類】')
st.sidebar.text(disease_list)


st.header('■疾患別一人当たり医療費(万円/年)(2022年)')

pref_list = r4_5_all.columns.values[1:]
option_pref = st.selectbox(
    '都道府県名',
    (pref_list))

#max_x = r4_5_all[option_pref].max()

fig = px.bar(r4_5_all,
            x=option_pref,
            y="疾患名",
            color="疾患名",
            range_x=[0,100000],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.text('出典：厚生労働省(医療費の地域差分析)')

#r4_5_graph = r4_5_graph.astype({'全国平均':float,'東京都':float})
#r4_5_graph.set_index('疾患名')
#st.line_chart(r4_5_graph)

#pref_list = r4_5_all['都道府県名']

#option_pref = st.selectbox(
#    '都道府県',
#    (pref_list))


#option_multi = st.multiselect(
#    '都道府県を選択して下さい(複数可)',
#    pref_list,
#    ['全国平均','東京都']
#)

#option_multi


#r4_5_all = r4_5_all.rename(columns={'全疾患平均': '全疾患合計'})
#x_axis = r4_5_all.iloc[0:0,1:]
#y_data = r4_5_all[(r4_5_all["都道府県名"] == option_pref)]
#y_data.iloc[0:0,1:] = y_data.iloc[0:0,1:].astype(float)
#y_data2 = y_data.transpose()


#st.bar_chart(y_data2)
#st.write(
#    px.line(x_axis, y_data, title="test")
#)