import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import json
from deep_pv_frontend.utils.processing import predict_to_map, plotly_map
import plotly.figure_factory as ff
import requests
import seaborn as sns
import random

# st.set_page_config(layout="wide")
API_PATH = 'https://deepcloud-vpmy6xoida-ew.a.run.app'
url = f'{API_PATH}/hood?'

random_locations = [
    ('36.807816370788494', '-119.78978954999349'),
    ('37.67754438383909', '-121.0097469608227'),
    ('37.6875054437373', '-120.99656446426388')
    ]

default_lon_lat = random.choice(random_locations)
default_lat = default_lon_lat[0]
default_lon = default_lon_lat[1]
key = 'AIzaSyDPPv3PNUdHNn-zuxyLPiMABKUW8yoPojc'
default_size = 3

#preloaded data
with open("first_try.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
preloaded = jsonObject

def display_data(results):
    df = pd.DataFrame(results)
    table_df = df[['name','lat', 'lon', 'area_correction', 'kWh_mon']]
    total_energy_output = df['kWh_mon'].sum().round()
    total_num_PV = len(df)
    average_energy_output = df['kWh_mon'].mean().round()

    col1, col2, col3 = st.columns(3)
    col1.metric(label = "No. panels in image", value =total_num_PV)
    col2.metric(label = "Monthly energy (kwh)", value =total_energy_output)
    col3.metric(label = "Av. energy (kWh)", value =average_energy_output)

    st.markdown(f"""These panels are sufficient to supply
                **<span style="background-color:#FFBF00">{int(total_energy_output / (2479/12))} households</span>**
                **each month** in the Netherlands at an average of 2.479/kWh.
                It also represents a monthly energy value of
                **<span style="background-color:#FFBF00">{int(0.7 * total_energy_output)}</span>**
                Euro, at an average of
                **<span style="background-color:#FFBF00">{int(0.7* average_energy_output)}</span>**
                Euro per panel constellation.""", unsafe_allow_html=True)

    with st.expander(f"Distribution of power output per panel detected"):
        fig, ax = plt.subplots(figsize=(6, 3))
        #set figure aesthetic
        sns.set(rc={'axes.facecolor':'#ECF0F1', 'figure.facecolor':'white','patch.edgecolor': 'w', 'grid.linestyle': '--', 'ytick.left': True, 'grid.color': '#BDC3C7'})
        sns.set_context("paper") #resolution of image
        #plot elements
        sns.histplot( data=pd.DataFrame(results)['kWh_mon'], bins = 10,  color = '#FFBF00')
        #plt.title("Distribution of power output per panel detected", fontsize = 14)
        plt.xlabel('kWh per month output', fontsize = 12)
        plt.ylabel('Number of panels', fontsize = 12)
        #display on streamlit
        st.pyplot(fig)
        # st.bar_chart(pd.DataFrame(results)['kWh_mon'])
    with st.expander(f"All analyzed solar panel data"):
        st.dataframe(table_df)

def get_custom_data():
    response = requests.get(url, params=params).json()
    results = response['results']
    map = predict_to_map(results)
    st.pydeck_chart(map)
    display_data(results)

def interactive_map():
    st.map()

######################## main interface ############

st.header("deep-pv")
st.markdown("Calculate energy generated by solar panels anywhere in the world using deep-learning☀️")

option = st.selectbox(
     'Select view',
     ('Custom', 'Rotterdam'))

if option == 'Custom':

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 4])
    cal = col1.button('Fresno (US)')
    unk = col2.button('Ketton (UK)')
    rot = col3.button('Rotterdam (NL)')
    mex = col4.button('CDMX (MX)')

    col1, col2 = st.columns(2)
    latitude = col1.text_input('latitude', default_lat)
    longitude = col1.text_input('longitude', default_lon)
    # key = col1.text_input('API Key', default_api)
    size = col1.slider('Map Size', 1, 9, default_size)
    col1.write("To make a prediction, select a location and we'll calculate your KPIs!")
    kpi = col1.button('Find my Panels!')
    params = {'latitude':latitude, 'longitude':longitude, 'key': key, 'size':size}

    if cal:
        cal = 0
        latitude = '36.807816370788494'
        longitude = '-119.78978954999349'
        print("getting cali")
        params = {'latitude':latitude, 'longitude':longitude, 'key': key, 'size':size}
        with st.spinner('We got Marcobot4000 looking in California! He is looking for panels'):
            get_custom_data()
            st.success('Done!')

    if rot:
        rot = 0
        latitude = '51.95658225956649'
        longitude = '4.472880279577454'
        print("getting rotterdam")
        params = {'latitude':latitude, 'longitude':longitude, 'key': key, 'size':size}
        with st.spinner('We got Marcobot4000 looking in Rotterdam! He is looking for panels'):
            get_custom_data()
            st.success('Done!')

    if unk:
        unk = 0
        latitude = '52.64414513320668'
        longitude = '-0.5584604495359557'
        print("getting ketton")
        params = {'latitude':latitude, 'longitude':longitude, 'key': key, 'size':size}
        with st.spinner('We got Marcobot4000 looking in Ketton! He is looking for panels..'):
            get_custom_data()
            st.success('Done!')

    if mex:
        mex = 0
        latitude = '19.35054518303481'
        longitude = '-99.19522683159232'
        print("getting mexico")
        params = {'latitude':latitude, 'longitude':longitude, 'key': key, 'size':size}
        with st.spinner('We got Marcobot4000 looking in Mexico City! He is looking for panels.'):
            get_custom_data()
            st.success('Done!')

    df = pd.DataFrame([[float(latitude), float(longitude)]],
     columns=['lat', 'lon'])
    col2.map(df)

    if kpi:
        with st.spinner('We got Marcobot4000 on it! Hes looking for panels'):
            get_custom_data()
            st.success('Done!')

elif option == 'Rotterdam':
    st.write("Solar panel data analysed from Rotterdam on 20km2 in June 2019")
    results = preloaded['results']
    map = plotly_map(scores = results)
    st.plotly_chart(map, use_container_width=True, sharing="streamlit")
    display_data(results)

# with st.sidebar.expander(f"About"):
#         st.write("""This project uses deep learning to identify and quantify solar panels anywhere in the world. It uses a Multi-Region Convolutional Neural Network (MRCNN) architecture trained on images in California and China.
#                  """)

# with st.sidebar.expander(f"Info for nerds"):
#         st.write("""An [MRCNN](https://github.com/matterport/Mask_RCNN) model was trained on an open source [California](https://www.nature.com/articles/sdata2016106) and [china](https://essd.copernicus.org/preprints/essd-2021-270/essd-2021-270.pdf) data set. All files were tiled in tiles of 256x256, with annotations in the [COCO format](https://cocodataset.org/#home). Mean Average Precision after training about 4000 tiles with 100 epochs reached (mAP) in-city = 90+
#         Mean Average Precision (mAP) cross-continent = +70 """)

# with st.sidebar.expander(f"Team"):
#         st.write("""Project team: Toby Winter, Mary Ward, Marco Rodriguez, Ivan Thung""")
