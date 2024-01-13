import numpy as np 
import pandas as pd 
import streamlit as st 
import pydeck as pdk
import plotly.express as px
from PIL import Image
import random


st.title('日本の医療オープンデータ解析DB')
tab_titles = ['サマリー','生活習慣との相関','TBC2']
tab1, tab2, tab3 = st.tabs(tab_titles)

with tab1:
    st.header('サマリー')
    st.write('<font size="4">本DB(ダッシュボード)は厚生労働省(医療費の地域差分析、2023年12月28日公表)やRESASの医療系オープンデータを加工して作成しております。</font>', unsafe_allow_html=True)
    st.write('  \n')

    image0 = Image.open('./pics/pic0.PNG')
    image1 = Image.open('./pics/pic1.PNG')
    image2 = Image.open('./pics/pic2.PNG')
    image3 = Image.open('./pics/pic3.PNG')
    image4 = Image.open('./pics/picc4.PNG')
    image5 = Image.open('./pics/pic5.PNG')
    image6 = Image.open('./pics/pic6.PNG')
    image7 = Image.open('./pics/pic7.PNG')

    image = [image0,image1,image2,image3,image4,image5,image6,image7]

    st.image(image[random.randint(0,7)])
    st.write('  \n')
    st.write('  \n')               
                    
    option_select = st.sidebar.selectbox(
        "【①②共通】対象とする保険制度を選択して下さい",
        ('全制度計','市町村国民健康保険','後期高齢者医療制度')
    )
    st.sidebar.write(option_select,'を選択中')

    r4_5 = []

    if option_select == '全制度計':
        r4_5 = pd.read_csv('./csv_data/r4-5all.csv')
        filename = '①都道府県別一人当たり医療費(円/年)(2022年)(全制度計).csv'
        filenameall = '①都道府県別一人当たり医療費(円/年)(2022年)(全制度計, 全データ).csv'
    elif option_select == '市町村国民健康保険':
        r4_5 = pd.read_csv('./csv_data/r4-5kokuho.csv')
        filename = '①都道府県別一人当たり医療費(円/年)(2022年)(国保).csv'
        filenameall = '①都道府県別一人当たり医療費(円/年)(2022年)(国保, 全データ).csv'
    else:
        r4_5 = pd.read_csv('./csv_data/r4-5kouki.csv')
        filename = '①都道府県別一人当たり医療費(円/年)(2022年)(後期).csv'
        filenameall = '①都道府県別一人当たり医療費(円/年)(2022年)(後期, 全データ).csv'

    pref_list = r4_5["都道府県名"]

    disease_list = pd.read_csv('./csv_data/厚労省疾患名リスト.csv')
    st.sidebar.header('【厚労省定義の疾患分類】')
    st.sidebar.write(disease_list, unsafe_allow_html=True)


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

    fig.update_layout(yaxis=dict(title='都道府県名',dtick=1))

    st.plotly_chart(fig)

    st.download_button(
        label="①CSVファイルのダウンロード(グラフ分)",
        data=r4_5[['都道府県名',option_disease]].to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
        file_name=filename,  # ダウンロードするファイル名を指定
        key='download-button1'
    )

    st.download_button(
        label="①CSVファイルのダウンロード(全データ)",
        data=r4_5.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
        file_name=filenameall,  # ダウンロードするファイル名を指定
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
        filename = '②疾患別一人当たり医療費(円/年)(2022年)(全制度計).csv'
        filenameall = '②疾患別一人当たり医療費(円/年)(2022年)(全制度計, 全データ).csv'
    elif option_select == '市町村国民健康保険':
        r4_5_t = pd.read_csv('./csv_data/r4-5kokuho-t.csv')
        filename = '②疾患別一人当たり医療費(円/年)(2022年)(国保).csv'
        filenameall = '②疾患別一人当たり医療費(円/年)(2022年)(国保, 全データ).csv'
    else:
        r4_5_t = pd.read_csv('./csv_data/r4-5kouki-t.csv')
        filename = '②疾患別一人当たり医療費(円/年)(2022年)(後期).csv'
        filenameall = '②疾患別一人当たり医療費(円/年)(2022年)(後期, 全データ).csv'

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
        file_name=filename,  # ダウンロードするファイル名を指定
        key='download-button2'
    )

    st.download_button(
        label="②CSVファイルのダウンロード(全データ)",
        data=r4_5_t.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
        file_name=filenameall,  # ダウンロードするファイル名を指定
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
        filename = '③疾患別患者数(入院, 2020年, 単位:千人).csv'
        filenameall = '③疾患別患者数(入院(全データ), 2020年, 単位:千人).csv'
        
    else:
        df_num_pat = pd.read_csv('./csv_data/num_outpatients.csv')
        filename = '③疾患別患者数(外来, 2020年, 単位:千人).csv'
        filenameall = '③疾患別患者数(外来(全データ), 2020年, 単位:千人).csv'

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
        file_name=filename,  # ダウンロードするファイル名を指定
        key='download-button3'
    )

    st.download_button(
        label="③CSVファイルのダウンロード(全データ)",
        data=df_num_pat.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
        file_name=filenameall,  # ダウンロードするファイル名を指定
        key='download-button3all'
    )

    st.write('<a href="https://resas.go.jp/medical-welfare-medical-analysis/">出典：RESAS(医療・福祉マップ(医療受給))</a>', unsafe_allow_html=True)
    st.write('  \n')
    st.write('  \n')
    st.write('  \n')
    st.write('  \n')

    st.subheader('④疾患別医師数/医療施設数(2020年)')

    option_hcp = st.selectbox(
        '医師数/10万人当たり医師数、もしくは病院数/一般診療所数を選択して下さい。',
        ['医師数', '10万人当たり医師数','病院数','一般診療所数'])

    if option_hcp == '医師数':
        df_num_hcp = pd.read_csv('./csv_data/num_doctors.csv')
        filename = '④疾患別医師数(2020年).csv'
        filenameall = '④疾患別医師数(2020年)(全データ).csv'

    elif option_hcp == '10万人当たり医師数': 
        df_num_hcp = pd.read_csv('./csv_data/num_doctors_per100k.csv')
        filename = '④疾患別医師数(10万人当たり)(2020年).csv'
        filenameall = '④疾患別医師数(10万人当たり)(全データ).csv'

    elif option_hcp == '病院数': 
        df_num_hcp = pd.read_csv('./csv_data/num_hospitals.csv')
        filename = '④疾患別病院数(2020年).csv'
        filenameall = '④疾患別病院数(2020年)(全データ).csv'

    else:
        df_num_hcp = pd.read_csv('./csv_data/num_clinics.csv')
        filename = '④疾患別一般診療所数(2020年).csv'
        filenameall = '④疾患別一般診療所数(2020年)(全データ).csv'

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
                height=800)
    st.plotly_chart(fig)

    fig.update_layout(yaxis=dict(title='',dtick=1))

    st.download_button(
        label="④CSVファイルのダウンロード(グラフ分)",
        data=df_num_hcp[['診療科',option_pref4]].to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
        file_name=filename,  # ダウンロードするファイル名を指定
        key='download-button4'
    )

    st.download_button(
        label="④CSVファイルのダウンロード(全データ)",
        data=df_num_hcp.to_csv().encode('utf-8'),  # データフレームをCSV形式に変換してエンコード
        file_name=filenameall,  # ダウンロードするファイル名を指定
        key='download-button4all'
    )

    st.write('<a href="https://resas.go.jp/medical-welfare-medical-analysis/">出典：RESAS(医療・福祉マップ(医療受給))</a>', unsafe_allow_html=True)
    st.write('  \n')
    st.write('  \n')
    st.write('<a href="mailto:tadahisa.terao777@gmail.com">お問合せ先はこちらまで(tadahisa.terao777@gmail.com)</a>', unsafe_allow_html=True)

with tab2:
    st.header('生活習慣との相関')
    st.write('各都道府県ごとのデータ(サマリータブ①で選択した疾患分類における一人当たり医療費(Y軸) X 各種生活習慣(飲酒量/喫煙率等)(X軸))をマッピングします。右肩上がりにマッピングされているほど、その生活習慣がその疾患の医療費に影響している(=相関が高い)ことを示しています。')

    sakeImg0 = Image.open('./pics/sake0.png')
    sakeImg1 = Image.open('./pics/sake1.PNG')
    sakeImg2 = Image.open('./pics/sake2.PNG')

    image2 = [sakeImg0,sakeImg1,sakeImg2]

    habits = pd.read_csv('./csv_data/habits.csv')
    correl = pd.merge(r4_5, habits, on='都道府県名')
    
    option_habits = st.selectbox(
        '一人当たり医療費との相関を調べたい生活習慣を選択して下さい',
        ['成人１人当たりの酒類消費量(ℓ/年,2021)','成人喫煙率(%,2019)']
        )

    st.image(image2[random.randint(0,2)])
    st.write('  \n')
    st.write('  \n') 
    
    s1 = correl[option_habits]
    s2 = correl[option_disease]
    res=s1.corr(s2)
    st.write('相関係数(-1~1)は',round(res,2),'です。1に近いほど正の相関、-1に近いほど負の相関を意味しています。0に近い場合はほぼ相関がないことを示しています。')
    
    mix_x = 0
    mix_x = int(correl[option_habits].min())*0.9

    max_x2 = 0
    max_x2 = int(correl[option_habits].max())*1.1

    mix_y = 0
    mix_y = int(correl[option_disease].min())*0.9

    max_y = 0
    max_y = int(correl[option_disease].max())*1.1

    fig = px.scatter(correl, x = option_habits,
                      y = option_disease, 
                      range_x = [mix_x, max_x2],
                      range_y = [mix_y, max_y],
                      size_max = 100,
                      color = '都道府県名'
                    )
    
    st.plotly_chart(fig)

    st.write('<a href="https://www.nta.go.jp/taxes/sake/shiori-gaikyo/shiori/2023/index.htm">出典：国税局 酒のしおり(令和5年6月)(販売(消費)数量)(2021年度)</a>', unsafe_allow_html=True)
    st.write('<a href="https://ganjoho.jp/reg_stat/statistics/data/dl/index.html#smoking">出典：国民生活基礎調査による都道府県別喫煙率データ(2019年度)</a>', unsafe_allow_html=True)
    st.write('  \n')

with tab３:
    st.header('To Be Continued...２')
    st.write('乞うご期待！')