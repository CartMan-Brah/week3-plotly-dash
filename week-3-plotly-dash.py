#!/usr/bin/env python
# coding: utf-8

# In[1]:


#install dash
get_ipython().system('pip install dash==1.19.0  ')

get_ipython().system('pip install jupyter_dash ')

get_ipython().system('pip install --upgrade plotly')


# In[2]:


# Import required libraries
import pandas as pd
import dash
from jupyter_dash import JupyterDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


# In[3]:


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# In[5]:


# Create a dash application
app = JupyterDash(__name__)


# In[15]:


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'site1'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'site2'},
                                                 {'label': 'KSC LC-39A', 'value': 'site3'},
                                                 {'label': 'VAFD SLC-4E', 'value': 'site4'}
                                                 ],
                                             value='ALL',
                                             placeholder="Launch site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',100: '100'},
                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    spacex_1_df=spacex_df
    if entered_site == 'All Sites':
        fig = px.pie(spacex_1_df, values='class', 
        names='Launch Site', 
        title='Total Successful Launches by Site')
        return fig
    else:
        spacex_1_df=spacex_df[spacex_df['Launch Site']==entered_site]
        spacex_1_df=spacex_1_df.groupby(['Launch Site','class']).size().reset_index(name='class count') 
        fig = px.pie(
            spacex_1_df, 
            values='class count',
            names='class',
            title='Total Successful Launches for Site' + entered_site
        )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def scatter(entered_site,payload):
    spacex_1_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
       
    if entered_site=='ALL':
        fig=px.scatter(spacex_1_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                       title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(spacex_1_df[spacex_1_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',
                      color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(mode='inline', port = 8090, dev_tools_ui=True, debug=True,dev_tools_hot_reload =True, threaded=True)


# In[ ]:




