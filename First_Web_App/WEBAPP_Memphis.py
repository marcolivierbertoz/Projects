import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import requests


# Writing title & description
st.write("""
# Memphis Parks
Here follow the first WEB App created with _Streamlit_.
The web app will show the location of different parks according to the user options that have been selected, accordying by ZipCode.

> Due for quickly development (and understading of the package), not all the Features are going to be used, and also, the data provided that show up in the map, are only the **ZipCode** and not the real postion of the park. 

> Video Tutorial followed from YouTube channell _SATSifaction_ : https://www.youtube.com/watch?v=vKRj7GiaiTY&t=21s

> Documentation consulted from _Streamlit_:https://docs.streamlit.io/en/stable/main_concepts.html#layout
""")


# Creating funciton to load the data and store it in the cache
@st.cache
def load_data():
    df=pd.read_csv('Memphis_Park.csv')
    return df

df = load_data() 
 




# Creating sidebar ######################################
st.sidebar.header('User Input Options')
# Sidebar option
params={
   #'Council_District': st.sidebar.selectbox('Council District',(1,2,3,4,5,6,7)),
   'Acres_park': st.sidebar.slider('Acres', min(df['Acres_park']), max(df['Acres_park']),(min(df['Acres_park']),max(df['Acres_park']))),
   'Ballfield': st.sidebar.radio('Ballfield',('yes','no')),
   'Basketball': st.sidebar.radio('Basketball',('yes','no')),
   'Concession': st.sidebar.radio('Concession',('yes','no')),
#    'Fountains': st.sidebar.radio('Fountains',('yes','no')),
#    'Grills': st.sidebar.radio('Grills',('yes','no')),
#    'Off_Street_Parking': st.sidebar.radio('Off Street Parking',('yes','no')),
#    'Pavilions': st.sidebar.radio('Pavilions',('yes','no')),
#    'Picnic_Tables': st.sidebar.radio('Picnic Tables',('yes','no')),
#    'Playground': st.sidebar.radio('Playground',('yes','no')),
#    'Pools': st.sidebar.radio('Pools',('yes','no')),
#    'Restrooms': st.sidebar.radio('Restrooms',('yes','no')),
#    'Tennis_Courts': st.sidebar.radio('Tennis_Courts',('yes','no')),
#    'Trash': st.sidebar.radio('Trash',('yes','no')),
#    'Walking_Trails': st.sidebar.radio('Walking Trails',('yes','no'))   



}
########################################################
# As described in the video
# Function for location
@st.cache
def get_locations(zipcode):
	url='https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&q={}&facet=state&facet=timezone&facet=dst'.format(zipcode)
	data=requests.get(url).json()
	lat=data['records'][0]['fields']['latitude']
	lng=data['records'][0]['fields']['longitude']
	return lat, lng
########################################################  


# def map_df(df):
# 	df=df[df['bedrooms']==params['bedrooms']]
# 	df=df[df['bathrooms']==params['bathrooms']]
# 	df=df[df['floors']==params['floors']]
#     df=df[df['Fountains'] == params['Fountains']]
# 	df=df[df['waterfront']==params['waterfront']]
# 	df=df[(df['sqft_living']>0.9*params['sqft']) & (df['sqft_living']<1.1*params['sqft'])]
# 	df.reset_index()
# 	df['lat']=[get_locations(df.iloc[[i]]['zip'].values.astype(int))[0] for i in range(len(df))]
# 	df['lon']=[get_locations(df.iloc[[i]]['zip'].values.astype(int))[1] for i in range(len(df))]
# 	return df

#########################################################  
# Function for filtering
def map_df(df):
	#df=df[df['Council_District'] == params['Council_District']]
	df=df[df['Ballfield'] == params['Ballfield']]
	df=df[df['Basketball'] == params['Basketball']]
	df=df[df['Concession'] == params['Concession']]
    #df=df[df['Fountains'] == params['Fountains']]
    #df=df[df['Grills'] == params['Grills']]
    # df=df[df['Off_Street_Parking'] == params['Off_Street_Parking']]
    # df=df[df['Pavilions'] == params['Pavilions']]
    # df=df[df['Picnic_Tables'] == params['Picnic_Tables']]
    # df=df[df['Playground'] == params['Playground']]
    # df=df[df['Pools'] == params['Pools']]
    # df=df[df['Restrooms'] == params['Restrooms']]
    # df=df[df['Tennis_Courts'] == params['Tennis_Courts']]
    # df=df[df['Trash'] == params['Trash']]
    # df=df[df['Walking_Trails'] == params['Walking_Trails']]
	df=df[(df['Acres_park'] == params['Acres_park'])]
	df.reset_index(inplace=True)
	df['lat']=[get_locations(df.iloc[[i]]['ZipCode'].values.astype(int))[0] for i in range(len(df))]
	df['lon']=[get_locations(df.iloc[[i]]['ZipCode'].values.astype(int))[1] for i in range(len(df))]
	return df

#########################################################

########################################################

# Creating running function
def run_data():
	df1=map_df(df)
	st.map(df1)
	df1

# Creating a Button
btn = st.sidebar.button("Visualize")   

if btn:
	run_data()
else:
	pass

#########################################################

