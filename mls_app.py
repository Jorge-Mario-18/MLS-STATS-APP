import streamlit as st
import numpy as np
import matplotlib.style
import matplotlib as plt
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import lxml
import html5lib
import seaborn as sns
import plotly.express as px
import time
import colorcet as cc

st.image("mls_crest.png")

st.title("2023 Table in the MLS")

st.write(
    "This dashboard contains general stats from Major League Soccer. "
    "The dashboard is broken up into four sections by conference:\n"
    '1) The leading teams in the categories of "Goals in Favor", "Goals Against", and "XG"\n'
    "2) A general stats table\n"
    '3) A section created using seaborn library showcasing "Goal Difference", "Goals Scored by team", and "Wins by team"\n'
    "4) A pairplot where you can combine different categories on a X-Y chart\n"
)


url_e = "https://fbref.com/en/comps/22/2023/2023-Major-League-Soccer-Stats"
r_e = requests.get(url_e)
soup_e = bs(r_e.content, features="lxml")
table_e = soup_e.find_all("table", id="results2023221Eastern-Conference_overall")
table_e = pd.read_html(str(table_e))
table_e = table_e[0]
table_e.index = table_e["Rk"]
table_e = table_e.drop(["Rk"], axis=True)
table_e = table_e.drop(["Notes"], axis=True)


url_w = "https://fbref.com/en/comps/22/2023/2023-Major-League-Soccer-Stats"
r_w = requests.get(url_w)
soup_w = bs(r_w.content, features="lxml")
table_w = soup_w.find_all("table", id="results2023221Western-Conference_overall")
table_w = pd.read_html(str(table_w))
table_w = table_w[0]
table_w.index = table_w["Rk"]
table_w = table_w.drop(["Rk"], axis=True)
table_w = table_w.drop(["Notes"], axis=True)

st.divider()
st.subheader("Eastern Conference")
col1, col2, col3 = st.columns(3)
a = table_e.query("GF == GF.max()")["Squad"]
b = table_e.query("GA == GA.max()")["Squad"]
c = table_e.query("xG == xG.max()")["Squad"]
col1.caption("Goals in Favor")
col1.write(a)
col2.caption("Goals Against")
col2.write(b)
col3.caption("XG")
col3.write(c)
st.divider()
st.subheader("Western Conference")

col4, col5, col6 = st.columns(3)
d = table_w.query("GF == GF.max()")["Squad"]
e = table_w.query("GA == GA.max()")["Squad"]
f = table_w.query("xG == xG.max()")["Squad"]
col4.caption("Goals in Favor")
col4.write(d)
col5.caption("Goals Against")
col5.write(e)
col6.caption("XG")
col6.write(f)


st.header("Easter Conference Standings")
st.write(table_e)

st.header("Western Conference Standings")
st.write(table_w)


st.divider()

st.write("*Scroll left or right to choose the different charts*")


@st.cache_data
def load_table(conf):
    fig = px.bar(
        conf,
        x=conf.Squad,
        y=conf.xG,
        title="XG",
        text=conf.xG,
        color=conf.xG,
        color_continuous_scale="ylgn",
        height=600,
    )
    fig.update_xaxes(tickangle=270)
    st.write(fig)


@st.cache_data
def load_gDF(conf):
    stuff = conf
    fig = px.bar(
        stuff,
        x=stuff.Squad,
        y=stuff.GD,
        title="Goal Difference : MLS 2023",
        text=stuff.GD,
        color=stuff.GD,
        color_continuous_scale="ylgn",
        height=600,
    )
    fig.update_xaxes(tickangle=270)
    st.write(fig)


@st.cache_data
def load_pie(conf):
    fig = px.pie(conf, values="GF", names="Squad", title="Share of total Goals scored")
    st.write(fig)


(
    tab1,
    tab2,
    tab3,
    tab4,
    tab5,
    tab6,
) = st.tabs(
    [
        "Eastern Conference xG",
        "Western Conference xG",
        "Eastern Conference Goals Scored",
        "Western Conference Goals Scored",
        "Eastern Conference Goal Difference",
        "Western Conference Goal Difference",
    ]
)


with tab1:
    st.header("Eastern Conference")
    load_table(table_e)

with tab2:
    st.header("Western Conference")
    load_table(table_w)

with tab3:
    st.header("Eastern Conference")
    load_pie(table_e)

with tab4:
    st.header("Western Conference")
    load_pie(table_w)

with tab5:
    st.header("Eastern Conference")
    load_gDF(table_e)

with tab6:
    st.header("Western Conference")
    load_gDF(table_w)


st.divider()

st.write(
    "Here you can create your own plot combining\n"
    "any of the categories below and see how they relate to each other.\n"
    "The results my surprise you.\n"
)

conference = st.radio(
    "Eastern or Western Conference:",
    ("Eastern", "Western"),
    index=0,
    horizontal=True,
)

if conference == "Eastern":
    conf = table_e

if conference == "Western":
    conf = table_w

x = str(
    st.radio(
        "X-Axis:",
        ("GF", "GA", "W", "D", "L", "MP", "xG", "Pts"),
        index=0,
        horizontal=True,
    )
)

y = str(
    st.radio(
        "Y-Axis:",
        ("GF", "GA", "W", "D", "L", "MP", "xG", "Pts"),
        index=0,
        horizontal=True,
    )
)

button3 = st.button("Submit selection")

st.divider()


@st.cache_data
def load_pair(conf, x, y):
    stuff = conf
    x = stuff[x]
    y = stuff[y]
    fig = px.scatter(
        conf,
        x=x,
        y=y,
        color="Squad",
        color_discrete_sequence=px.colors.qualitative.Light24,
    )
    fig.update_traces(marker={"size": 15})
    st.write(fig)


if button3:
    with st.spinner("Who will win the MLS Cup....."):
        time.sleep(5)
    load_pair(conf, x, y)


st.write("*Data is provided by Sports-Reference.com*")
st.write("Jorge Mario Restrepo")
st.write("*Contact*")
st.write("Email: manizaleno_18@hotmail.com\n")
st.write("Linkedin: www.linkedin.com/in/jorgemariorest\n")
