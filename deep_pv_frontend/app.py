import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import json
from deep_pv_frontend.utils.processing import predict_to_map

# @st.cache
# predict all images to a bucket and return the stuff.
st.set_page_config(layout="wide")
col1, col2 = st.columns((4, 1))
col2.header("kpi")
col1.header("deep-pv")

latitude = st.sidebar.text_input('latitude', '51.927682071121296')
longitude = st.sidebar.text_input('longitude', '4.46474167449461')
key = st.sidebar.text_input('API Key')
kpi = st.sidebar.button('Generate KPIs')

API_PATH = 'https://deepcloud-vpmy6xoida-ew.a.run.app'
url = f'{API_PATH}/hood?'
params = {'latitude':latitude, 'longitude':longitude, 'key': key,}


# dummy run
with open("first_try.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
results = jsonObject

if kpi:

    params = {'latitude':latitude, 'longitude':longitude, 'key':key , 'size':1}
    #scores_dict = requests.get(url, params=params)

    url = f'{API_PATH}/hood?'
    results = results['results']
    map = predict_to_map(results)
    col1.pydeck_chart(map)

    #very basic plot

    # fig, ax = plt.subplots(figsize=(6, 2))
    # ax.hist(pd.DataFrame(results)['kWh_mon'].apply(round), bins = 20)
    # plt.title("Distribution of power output per panel detected")
    # plt.xlabel('kWh per Month output')
    # plt.ylabel('Frequency')
    # plt.show()
    # col1.pyplot(fig)

    df = pd.DataFrame(results)
    table_df = df[['name','lat', 'lon', 'area_correction', 'kWh_mon']]
    total_energy_output = df['kWh_mon'].sum().round()
    total_num_PV = len(df)
    average_energy_output = df['kWh_mon'].mean().round()

    with st.expander(f"All analyzed solar panel data of lat: {round(float(latitude), 4)} lon: {round(float(longitude),4)} "):
        st.write(table_df)

    col2.metric(label = "Total energy output", value =total_energy_output)
    col2.metric(label = "Av. energy (kWh)", value =average_energy_output)
