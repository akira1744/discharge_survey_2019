import streamlit as st
import altair as alt
from altair import limit_rows, to_values
import toolz
from package import myfunc


def t(data): return toolz.curried.pipe(
    data, limit_rows(max_rows=60000000), to_values)  # TODO データ最適化後、最大行数のミニマム化


st.set_page_config(layout="wide")

alt.data_transformers.register('custom', t)
alt.data_transformers.enable('custom')

hp, hp_list, pref_list, mdc2d, mdc6d, oped = myfunc.load_data()

st.sidebar.markdown("### 病院・疾患・手術別　患者数分析")

select_hpname = st.sidebar.multiselect('医療機関名', hp_list)

select_prefs, select_med2s, select_citys, hp = myfunc.set_location(
    select_hpname, hp, pref_list)

set_min, set_max = st.sidebar.slider("病床数", value=(0, 1400), step=50)

mdc2d, mdc6d, oped, hp = myfunc.filtering_data(
    hp, select_hpname, mdc2d, mdc6d, oped, set_min, set_max)

charts = myfunc.draw_chart(
    select_hpname,  mdc2d, mdc6d, oped, hp)

st.altair_chart(charts)


# フッター　###################################################################################
link1 = 'https://www.mhlw.go.jp/stf/shingi2/0000196043_00004.html'
link2 = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000198757.html'
link3 = 'https://www.e-stat.go.jp/stat-search/files?page=1&query=%E7%97%85%E9%99%A2%E6%95%B0%E3%80%80%E7%97%85%E5%BA%8A%E6%95%B0%E3%80%80%E4%BA%8C%E6%AC%A1%E5%8C%BB%E7%99%82%E5%9C%8F&sort=open_date%20desc&layout=dataset&stat_infid=000031982297&metadata=1&data=1'

my_expander = st.expander('DataSource')
with my_expander:
    st.markdown(
        '[1.令和元年度DPC導入の影響評価に係る調査「退院患者調査」の結果報告について]({})'.format(link1))
    st.markdown(
        '[2.診断群分類（DPC）電子点数表について]({})（診断群分類（DPC）電子点数表（令和元年5月22日更新） '.format(link2))
    st.markdown('[3.医療施設調査 / 令和元年医療施設（動態）調査 二次医療圏・市区町村編]({})'.format(link3))

my_expander = st.expander('Q & A')
with my_expander:
    st.markdown('Q1. 2020年度のデータは見れないか？')
    st.markdown('A1. 例年通りであれば2022年3月にデータが公開されます。公開され次第同様のホームページを作成します')
    st.markdown(' ')
    st.markdown('Q2. 院内の実績値と異なる')
    st.markdown('''
    A2. 厚労省の退院患者調査では、実績が10件未満のデータが公開されていない為、実績値よりも低い数字が表示されます。\n
    　　MDC6を選択している時は、疾患別手術別集計（参考資料２（８））の集計値が表示されます。\n
    　　MDC6を選択していない時は、MDC別医療機関別件数（参考資料２（２））の集計値が表示されます。
    '''
                )
# @@@
st.markdown('***')
st.markdown(
    "Thanks for going through this mini-analysis with me! I'd love feedback on this, so if you want to reach out you can find me on [twitter] (https://twitter.com/inakichii).")
