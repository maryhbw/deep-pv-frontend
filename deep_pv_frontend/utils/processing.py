import numpy as np
from google.cloud import storage
import pydeck as pdk
import pandas as pd
import plotly.express as px

def make_map(bbs, points):
    """Display a map centered at the mean lat/lon of the query set."""
    # Adding code so we can have map default to the center of the data
    bbs = pd.DataFrame(bbs)
    points = pd.DataFrame(points)
    midpoint = (np.average(points.lat), np.average(points.lon))

    initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=17)

    layer1 = pdk.Layer(
        "PolygonLayer",
        bbs,
        opacity=1,
        get_polygon="geometry",
        filled=False,
        getLineWidth=.5,
        extruded=False,
        wireframe=True,
        get_line_color=[255,255,0],
        auto_highlight=True,
        pickable=True,
        )

    points['pointsize'] = points['area'] / 10
    layer2 = pdk.Layer(
                'ScatterplotLayer',
                data=points,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius='pointsize',
                stroked=True,
                pickable=True
                )
    #Create labeled map
    labeled_map = pdk.Deck(layers=[layer1],
                           initial_view_state=initial_view_state,
                           map_style='mapbox://styles/mapbox/satellite-v9')
    return labeled_map

def scores_to_points(scores):
    return [{
        'name': s['name'],
        'lat': s['lat'],
        'lon': s['lon'],
        'area': s['area']
        } for s in scores ]

def scores_to_bb(scores):
    return [{
        'name': s['name'],
        'geometry': s['bb_latlon'],
        'confidence': s['score']
        } for s in scores ]

def plotly_map(scores):
    scores = pd.DataFrame(scores)
    scores['count'] = 1
    midpoint = (np.average(scores['lat']), np.average(scores['lon']))
    center = {'lat': midpoint[0],'lon':midpoint[1]}
    fig = px.density_mapbox(scores, lat='lat', lon='lon', z='count',
                        mapbox_style="carto-positron", center = center, zoom = 17, width = 100)
#use groupby to transform data from wide to short for heatmap application
    return fig
def make_results(scores):
    points = scores_to_points(scores)

def predict_to_map(scores):
    bbs = scores_to_bb(scores)
    points = scores_to_points(scores)
    map = make_map(bbs, points)
    return map
