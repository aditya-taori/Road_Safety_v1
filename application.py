#Importing necessary libraries
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import pydeck as pdk
import dash_auth

dash_app = dash.Dash()  #creating a dash object

app = dash_app.server  


dash_app.config.suppress_callback_exceptions = True  #For not triggering the exceptions

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   #CSS File to be included

#Authentication
#To put an authentication on the dash application
auth = dash_auth.BasicAuth(
    dash_app,
    (('ak1','1234',),)
)

#Layout of the dash app

#rendering the layout of the page on the basis of the selected url

dash_app.layout = html.Div([
    html.Div(" "),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#Main Page / Home page of the websote
index_page = html.Div([
     html.H1('ERM Road Safety'),
    html.Img(src= '/assets/Road_Safety_v1.PNG',width = 1800, height= 300),
    html.Br(),
    html.Br(),
    dcc.Link('Alarms Overview', href='/Overview') ,
    html.Br(),
     html.Br(),
    dcc.Link('Dynamic Crash Prevention System', href='/DCP'),
    html.Br()
])


# Render the page on the basis of the url
@dash_app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Overview':  #if url is observations then render the layout of Safety Observations
        return Overview_layout
    elif pathname == '/DCP':  #If url is Incident then render the layout of Safety Incidents 
        return DCP_Layout
    else:
        return index_page  #Otherwise for other inputs always show the index page
    
    # You could also return a 404 "URL not found" page here


hm_data = pd.read_csv("C:/Users/Aditya.Taori/ERM Python Codes/Road Safety/Shell Demo/Datasets/Heatmap_Data.csv")
unique_categories = hm_data["Category Alarms"].unique()
    

Overview_layout = html.Div([html.H1('ERM Road Safety'),  #Heading
                        html.H2('Alarms Overview'),
                        html.Img(src= '/assets/Overview_Image.jpg',width = 1800, height= 300),
                        html.Br(),  #Line Break
                        html.Br(),  #Line Break
                        dcc.Link('Main Page', href='/'), #Hyperlink in the webpage
                        html.Br(),
                        html.H2("HeatMap of Alarms"),
                        dcc.Dropdown(
                            id = "demo-dropdown",
                            options=[{'label':i,'value':i} for i in unique_categories],
                            multi=True,
                                ),
                        html.Div(id="Heatmap_Catgeories",style = {'width':1800,'height':500}),
                        html.Br(),  #Line Break
                        html.Br(),  #Line Break
                        html.H2("Spread of Alarms Location wise"),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Tambon Khlong Kiu', 'value': 'TKK'},
                                {'label': 'Tambon Map Kha', 'value': 'TMK'},
                                {'label': 'Tambon Muang Wan', 'value': 'TMW'},
                                {'label': 'Bang Muang','value':'BM'}
                            ],
                            multi=True,
                            value="TMK"
                        ),
                        html.Div(id="LocatioDrivern_alarms",style = {'width':1800,'height':500}),
                        html.Br(),  #Line Break
                        html.Br(),  #Line Break
                        html.H2("Route Maps Contract wise "),
                        dcc.Dropdown(
                            options=[
                                {'label': 'King Kaew (V2)', 'value': 'KKV2'},
                                {'label': 'LNG (V2)', 'value': 'LNGV2'},
                                {'label': 'Bangbung (V2)', 'value': 'BV2'}
                            ],
                            multi=True,
                            value="LNGV2"
                        ),
                        html.Div(id="Route Maps",style = {'width':1800,'height':500}),
                        html.Br(),  #Line Break
                        html.Br(),  #Line Break
                    
])

DCP_Layout = html.Div([
                        html.H1('ERM Road Safety'),  #Heading
                        html.H2('Dynamic Crash Prevention System'),
                        html.Img(src= '/assets/DCP_Image.png',width = 1800, height= 300),
                        html.Br(),  #Line Break
                        html.Br(),  #Line Break
                        dcc.Link('Main Page', href='/'), #Hyperlink in the webpage
                        html.Br(),
                        html.H2("Select Contractor"),
                        dcc.Dropdown(
                            options=[
                                {'label': 'King Kaew (V2)', 'value': 'KKV2'},
                                {'label': 'LNG (V2)', 'value': 'LNGV2'},
                                {'label': 'Bangbung (V2)', 'value': 'BV2'}
                            ],
                            multi=True,
                            value="LNGV2"
                        ),
                        html.Br(),
                        html.H2("Select Vehicle"),
                        dcc.Dropdown(
                            options=[
                                {'label': 'DR-142-53', 'value': 'V1'},
                                {'label': 'DR-143-67', 'value': 'V2'},
                                {'label': 'DR-134-21', 'value': 'V3'},
                                {'label': 'DR-137-22', 'value': 'V4'}
                            ],
                            multi=True,
                            value="LNGV2"
                        ),
                        html.Br(),
                        html.Div(id="Live Location")
])

@dash_app.callback(
    dash.dependencies.Output('Heatmap_Catgeories', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    if value != None:
        print(len(value))
        sub_data= hm_data[hm_data["Category Alarms"].isin(value)]
        print(sub_data)
        layer = pdk.Layer(
            'HeatmapLayer',     # Change the `type` positional argument here
            sub_data,
            get_position='[Longitude,Latitude]',
            get_weight = '[Weight]',
            pickable=True,
            radius_pixels= 30,
            auto_highlight=True)

        # Set the viewport location
        view_state = pdk.ViewState(
          longitude=sub_data["Longitude"].iloc[0],
          latitude= sub_data["Latitude"].iloc[0],
          zoom= 9,
          maxZoom= 20,
          pitch= 0,
          bearing= 0,
          minZom = 5)



        key_api = "pk.eyJ1IjoiYWRpdHlhdGFvcmkiLCJhIjoiY2s1NTMzM205MGJyNjNla2JxZDRxdHBvdiJ9.OmOHzC_AyvWfjv9Sulz3tw" 

        # Render
        r = pdk.Deck(layers=[layer], initial_view_state=view_state,mapbox_key=key_api,map_style = "mapbox://styles/mapbox/dark-v9")

        r.to_html("assets/Heatmap_Layer.html",notebook_display=False)
    #hm_data[(hm_data["Category Alarms"]==
        return html.Div([
                html.Iframe(src = dash_app.get_asset_url("Heatmap_Layer.html"),width=1800,height = 600)
        ])


if __name__ == '__main__':
    dash_app.run_server()
