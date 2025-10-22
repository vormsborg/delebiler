import streamlit as st
import math
import json
import os
from pathlib import Path
import sys

import pandas as pd
import plotly.express as px

FILE_DIR    = os.path.abspath(__file__)
PROJECT_DIR = Path(FILE_DIR).parent.parent
DATA_PATH   = PROJECT_DIR / 'data' / 'priser.json'

sys.path.append(str(PROJECT_DIR))

import scripts.pricing_models as pm

st.header("OBS. Under udvikling - Priser ikke opdaterede.")
#%% LOAD DATA
with open(DATA_PATH, 'r') as json_file:
    data = json.load(json_file)

#%% USER INPUT
with st.sidebar:
    hours = st.slider('timer', 0, 23)
    km    = st.number_input('km', step = 1)
    days  = st.slider('dage', 0, 6)
    weeks  = st.number_input('uger', step = 1)








#%% POPULATE CLASSES AND CALCULATE PRICES

results_list = []


for entry in data:


    cars_data = entry['biler']

    for car in cars_data:
        # Generate object       
        Object = None
        if entry['firma'] == 'Kinto':

            Object = pm.KintoModel(
                car['model'],
                car['pris_pr_time'],
                car['pris_pr_dgn'],
                car['pris_pr_uge'],
                car['pris_pr_km']
            )

        elif entry['firma'] == 'Hyre':
            Object = pm.HyreModel(
                car['model'],
                car['pris_pr_time'],
                car['pris_pr_dgn'],
                car['pris_pr_uge'],
                car['pris_pr_km'],
                car['braendstof_pr_km'],
                car['gratis_km_pr_dgn'],
            )

        elif entry['firma'] == 'LetsGo':
            Object = pm.LetsgoModel(
                car['model'],
                car['pris_pr_time'],
                car['pris_pr_dgn'],
                car['pris_pr_uge'],
                car['pris_pr_km'],
                car['bestillingsgebyr'],                
            )

        elif entry['firma'] == 'Nordsjaellands Delebiler':
            Object = pm.NordsjaellandsDelebilerModel(
                car['model'],
                car['pris_pr_time'],
                car['pris_pr_km'],
                car['pris_pr_time_efter_12_timer'],
                car['pris_pr_km_efter_100_km'],                               
            )

        if not Object==None:
            # Calculate total price
            total_price = Object.calculate_total_price(
                hours=hours,
                days =days,
                weeks=weeks,
                km   =km
            )

            # Create results object
            ResultsObject = pm.TotalPrice(
                company     = entry['firma'],
                car_model   = Object.model,
                total_price = total_price
            )

            # Add results object to results list
            results_list.append(ResultsObject)


#%% CREATING A DATAFRAME

df = pd.DataFrame()
for result in results_list:
    df = pd.concat([df, pd.DataFrame.from_dict(result.__dict__, orient='index').T])

with st.expander('Data Tabular'):
    st.write(df.reset_index().drop(columns=['index']))

#%% PLOTTING

fig = px.histogram(
    df,
    x='company',
    y='total_price',
    color='car_model', barmode='group',
    title = "",
    # barmode='car_model'
)
st.plotly_chart(fig)