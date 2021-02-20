# Loading packages ##########################################################################
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
###############################################################################################
st.set_page_config(layout="wide")

# Loading the data set
@st.cache
def load_data():
    data=pd.read_csv('Mass_Shooting_Complete.csv')
    return data

mass_shooting_df = load_data() 
code = mass_shooting_df['Code']

# Creating sidebar ########################################################################
st.sidebar.title('Mass Shooting')
st.sidebar.write('This dashboard it is an evolution of an statistical school project, the aim of the dashboard is to show up the events of mass shooting in the USA')
st.sidebar.write('>Data Source: https://www.gunviolencearchive.org/mass-shooting')

# Map Control ########################################
st.sidebar.header('Map Control')
radio_selection= st.sidebar.radio('Select what you want to see on the map', ('Killed','Injured'))
######################################################

# Graphs control #####################################
st.sidebar.header('Graphs Control')

# Creating select box for state
state_select = st.sidebar.selectbox('Select a State', sorted(mass_shooting_df['State'].unique()))

# Retrive the selected state
state_data = mass_shooting_df[mass_shooting_df['State'] == state_select]
# Create select box for City or County
city_select = st.sidebar.selectbox('Select a City or County', sorted(state_data['City Or County'].unique()))
# Retrive selected city or county
city_data = state_data[state_data['City Or County'] == city_select]
#######################################################

#############################################################################################

## Setting column #######################################################################
left_column1, right_column1 = st.beta_columns(2)


## Left Column 1 ######################################################################
left_column1.header('Horizontal Barplot of States')
left_column1.write('Here will be show an horizontal barplot with the number of events of each states')

state_event = pd.DataFrame(mass_shooting_df['State'].value_counts()).sort_values(by=['State'])
fig_bar_state = px.bar(state_event, x='State', y=state_event.index, orientation='h')
left_column1.plotly_chart(fig_bar_state)

#######################################################################################


### Right Column 1 ###################################################################3
right_column1.header('Animations from 2014')
right_column1.write('Here it will appear the animation of the selected object form 2014')
if radio_selection == 'Killed':
    fig = px.choropleth(mass_shooting_df,
        locations=code,
        color='# Killed',
        hover_name='State',
        animation_frame='Incident Date',
        locationmode='USA-states'
    )

    fig.update_layout(
        geo_scope='usa'
    )

    right_column1.plotly_chart(fig)
elif radio_selection == 'Injured':
    fig = px.choropleth(mass_shooting_df,
        locations=code,
        color='# Injured',
        hover_name='State',
        animation_frame='Incident Date',
        locationmode='USA-states'
    )

    fig.update_layout(
        geo_scope='usa'
    )

    right_column1.plotly_chart(fig)

######################################################################################
#     
##########################################################################################
# Creating columns for two different plots ###############################################

left_column2, right_column2 = st.beta_columns(2)

## Left Column 1 ###########################
left_column2.header('Horizontal Barplot')
left_column2.write('Here are the Citiy or County of the State with the Total of Incidents')

# Creating barplot for the state
count_city = pd.DataFrame(state_data['City Or County'].value_counts()).sort_values(by=['City Or County'])
fig_bar = px.bar(count_city, x='City Or County', y=count_city.index, orientation='h')
left_column2.plotly_chart(fig_bar)

##########################################



## Right Column 2 ##########################
right_column2.header('Lineplot')
right_column2.write('Here there are two line plot with the # Killed & # Injured')

if st.sidebar.checkbox('Show lineplot for selected Citiy or County', True, key=1):
    fig_line_injured = px.line(city_data, x='Incident Date', y=['# Killed','# Injured'])
    right_column2.plotly_chart(fig_line_injured)
else: 
    fig_line_injured = px.line(state_data, x='Incident Date', y=['# Killed','# Injured'])
    right_column2.plotly_chart(fig_line_injured)

################################################################

#########################################

#############################################################################################

