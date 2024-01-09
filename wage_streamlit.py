import numpy as np 
import pandas as pd 
import streamlit as st 
import pydeck as pdk
import plotly.express as px
from PIL import Image

st.title('日本の医療オープンデータ解析DB')
st.write('  \n')

st.write('<font size="4">本DB(ダッシュボード)は厚生労働省(医療費の地域差分析)やRESASの医療系オープンデータを加工して作成しております。</font>', unsafe_allow_html=True)
st.write('  \n')

image = Image.open('futureHospital.png')
st.image(image)
st.write('  \n')
st.write('  \n')               
                   
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
st.sidebar.write(disease_list['疾患分類'], unsafe_allow_html=True)

hcp_dev_list = pd.read_csv('./csv_data/hcp_dev_list.csv')
st.sidebar.header('【RESAS定義の診療科】')
st.sidebar.write(hcp_dev_list, unsafe_allow_html=True)

st.subheader('①都道府県別一人当たり医療費(円/年)(2022年)')

#disease_list.insert(0,0,'疾患合計')
#r4_5.set_axis(disease_list, axis=1)

disease_list2 = r4_5.columns.values[1:]

option_disease = st.selectbox(
    '疾患分類を選択して下さい。',
    (disease_list2))

max_x = 0
max_x = int(r4_5[option_disease].max())

fig = px.bar(r4_5,
            x=option_disease,
            y="都道府県名",
            color="都道府県名",
            range_x=[0,max_x],
            orientation='h',
            width=800,
            height=800)
st.plotly_chart(fig)

st.download_button(
    label="①CSVファイルのダウンロード(グラフ分)",
    data=r4_5[['都道府県名',option_disease]].to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='rawdata.csv',  # ダウンロードするファイル名を指定
    key='download-button1'
)

st.download_button(
    label="①CSVファイルのダウンロード(全データ)",
    data=r4_5.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='allrawdata1.csv',  # ダウンロードするファイル名を指定
    key='download-button1all'
)

st.write('<a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryouhoken/database/iryomap/index.html">出典：厚生労働省(医療費の地域差分析)(2023年12月28日公表)</a>', unsafe_allow_html=True)
st.write('  \n')
st.write('  \n')
st.write('  \n')
st.write('  \n')


st.subheader('②疾患別一人当たり医療費(円/年)(2022年)')

r4_5_t = []

if option_select == '全制度計':
    r4_5_t = pd.read_csv('./csv_data/r4-5all-t.csv')
elif option_select == '市町村国民健康保険':
    r4_5_t = pd.read_csv('./csv_data/r4-5kokuho-t.csv')
else:
    r4_5_t = pd.read_csv('./csv_data/r4-5kouki-t.csv')

option_pref = st.selectbox(
    '都道府県名を選択して下さい。',
    (pref_list))

max_x2 = 0
max_x2 = int(r4_5_t[option_pref].max())

fig = px.bar(r4_5_t,
            x=option_pref,
            y="疾患名",
            color="疾患名",
            range_x=[0,max_x2],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.download_button(
    label="②CSVファイルのダウンロード(グラフ分)",
    data=r4_5_t[['疾患名',option_pref]].to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='rawdata.csv',  # ダウンロードするファイル名を指定
    key='download-button2'
)

st.download_button(
    label="②CSVファイルのダウンロード(全データ)",
    data=r4_5_t.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='allrawdata2.csv',  # ダウンロードするファイル名を指定
    key='download-button2all'
)

st.write('<a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/iryouhoken/database/iryomap/index.html">出典：厚生労働省(医療費の地域差分析)(2023年12月28日公表)</a>', unsafe_allow_html=True)
st.write('  \n')
st.write('  \n')
st.write('  \n')
st.write('  \n')


st.subheader('③疾患別患者数(入院/外来(単位:千人))(2020年)')

option_inorout = st.selectbox(
    '入院 or 外来を選択して下さい。',
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

st.download_button(
    label="③CSVファイルのダウンロード(グラフ分)",
    data=df_num_pat[['疾患分類',option_pref3]].to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='rawdata.csv',  # ダウンロードするファイル名を指定
    key='download-button3'
)

st.download_button(
    label="③CSVファイルのダウンロード(全データ)",
    data=df_num_pat.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='allrawdata3.csv',  # ダウンロードするファイル名を指定
    key='download-button3all'
)

st.write('<a href="https://resas.go.jp/medical-welfare-medical-analysis/">出典：RESAS(医療・福祉マップ(医療受給))</a>', unsafe_allow_html=True)
st.write('  \n')
st.write('  \n')
st.write('  \n')
st.write('  \n')

st.subheader('④疾患別医師数/医療施設数(2020年)')

option_hcp = st.selectbox(
    '医師数もしくは病院数、一般診療所数を選択して下さい。',
    ['医師数', '病院数','一般診療所数'])

if option_hcp == '医師数':
    df_num_hcp = pd.read_csv('./csv_data/num_doctors.csv')

elif option_hcp == '病院数': 
    df_num_hcp = pd.read_csv('./csv_data/num_hospitals.csv')

else:
    df_num_hcp = pd.read_csv('./csv_data/num_clinics.csv')

pref_list4 = df_num_hcp.columns.values[1:]

option_pref4 = st.selectbox(
    '都道府県を選択して下さい。',
    (pref_list4))

max_x4 = 0
max_x4 = int(df_num_hcp[option_pref4].max())

fig = px.bar(df_num_hcp,
            x=option_pref4,
            y="診療科",
            color="診療科",
            range_x=[0,max_x4],
            orientation='h',
            width=800,
            height=600)
st.plotly_chart(fig)

st.download_button(
    label="④CSVファイルのダウンロード(グラフ分)",
    data=df_num_hcp[['診療科',option_pref4]].to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='rawdata.csv',  # ダウンロードするファイル名を指定
    key='download-button4'
)

st.download_button(
    label="④CSVファイルのダウンロード(全データ)",
    data=df_num_hcp.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
    file_name='allrawdata4.csv',  # ダウンロードするファイル名を指定
    key='download-button4all'
)

st.write('<a href="https://resas.go.jp/medical-welfare-medical-analysis/">出典：RESAS(医療・福祉マップ(医療受給))</a>', unsafe_allow_html=True)
st.write('  \n')
st.write('  \n')
st.write('<a href="mailto:tadahisa.terao777@gmail.com">お問合せ先はこちらまで(tadahisa.terao777@gmail.com)</a>', unsafe_allow_html=True)