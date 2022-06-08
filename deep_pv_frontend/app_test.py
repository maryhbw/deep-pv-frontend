import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import json

# @st.cache
# predict all images to a bucket and return the stuff.
st.set_page_config(layout="wide")
col1, col2 = st.columns((4, 1))
col2.header("Logs")
col1.header("DEEP-PV")
col1.markdown("Get solar panel stats from any place in the world. \n 1. Define location. \n 2. Add API key. ")



latitude = col1.text_input('latitude')
longitude = col1.text_input('longitude')
key = col1.text_input('API Key')
API_PATH = 'https://deepcloud-vpmy6xoida-ew.a.run.app'
url = f'{API_PATH}/hood?'

clicked = col1.button('Click for heat map')
kpi = col1.button('Generate KPIs')
params = {'latitude':latitude, 'longitude':longitude, 'key':key , 'size':1}
with open("first_try.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
scores_dict = jsonObject

if kpi:
    #scores_dict = requests.get(url, params=params)
    print(scores_dict)
    scores_dict = scores_dict['results']
    print(len(scores_dict))
    # bucket_name = BUCKET_NAME
    # lats, lons, image_names = get_images_gcp(BUCKET_NAME, prefix = 'data/Rotterdam/PV Present/')
    url = f'{API_PATH}/hood?'


    fig, ax = plt.subplots(figsize=(6, 2))
    ax.hist(pd.DataFrame(scores_dict)['kWh_mon'].apply(round), bins = 20)
    plt.title("Distribution of power output per panel detected")
    plt.xlabel('kWh per Month output')
    plt.ylabel('Frequency')
    plt.show()
    col1.pyplot(fig)

    df = pd.DataFrame(scores_dict)
    total_energy_output = df['kWh_mon'].sum().round()
    total_num_PV = len(df)
    average_energy_output = df['kWh_mon'].mean().round()


if clicked:

    #"""Display a map centered at the mean lat/lon of the query set."""
    # Adding code so we can have map default to the center of the data
    df['lat'] = df['lat'].astype('float')
    df['lon'] = df['lon'].astype('float')
    midpoint = (np.average(df['lat']), np.average(df['lon']))

    initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=11)

    print(df.head())
    layer2 = pdk.Layer(
                'ScatterplotLayer',
                data= df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=40)

    #Render
    labeled_map = pdk.Deck(layers=[layer2], initial_view_state=initial_view_state)
    col1.pydeck_chart(labeled_map)
