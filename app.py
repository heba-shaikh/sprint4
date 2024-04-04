# %%
# import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# %%
# read in csv file & view first 5 rows
df = pd.read_csv("data.csv")

# %%
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app
server=app.server

# %%
states = df['State'].unique() #Creates list of states 
zipcodes = df['ZIP Code'].unique() #Creates list of zipcodes
conditions = df["Condition"].unique()

app.layout = html.Div([    
    html.H1("Hospital's Near You Dashboard"),  #Header for title
    html.P("Select the state and/or zipcode that you would like to find a hospital in. Also, select the condition you are going to the hospital for. Based on these parameters, you will be given a hospital list and measure name that is scored based on your condition. The higher the score, the better the hospital would be.",
           style={"color": "gray"}), #description under title
    dcc.Dropdown(      #use dcc to create dropdown menu
        id='state-dropdown',      #ID tag for dropdown
        options=[{'label': state, 'value': state} for state in states],   #specifies to go through each state in the dataframe as the options for the dropdown
        multi=False,     #allows to click single state
        placeholder="Select State",   #name of the dropdown before state is selected
        className= "twelve columns",      #formats dropdown to be on left half of screen
        style={"margin-bottom": "120px"}

),
    dcc.Dropdown(      #use dcc to create dropdown menu
        id='zipcode-dropdown',      #ID tag for dropdown
        multi=True,     #allows to click multiple zipcodes
        placeholder="Select Zipcode",   #name of the dropdown before zipcodes are selected
        className= "twelve columns",                   #formats dropdown to be on right half of screen
        style={"margin-bottom": "120px"}
),
    html.P("Enter Condition:"),
dcc.RadioItems(
        id='condition-dropdown',
        options = [{'label': condition, 'value': condition} for condition in conditions],
        className= "twelve columns"    ),
    dcc.Graph(
        id="Bar-Graph",
        className="twelve columns"
    )
    ])

#Callbacks
@app.callback(
    Output('zipcode-dropdown', 'options'),
    Input('state-dropdown', 'value')
)
def update_zipcodes(selected_state):   #To update zipcode selection list based on state that is selected
    if selected_state is None:
        return []
    else:
        zipcodes = df[df['State'] == selected_state]['ZIP Code'].unique()
        return [{'label': zipcode, 'value': zipcode} for zipcode in zipcodes]
@app.callback(
    Output('Bar-Graph', 'figure'),
    Input('state-dropdown', 'value'),
    Input('zipcode-dropdown', 'value'),
    Input('condition-dropdown', 'value')
)
def update_graph(selected_state, selected_zipcodes, selected_condition):
    filtered_df = df.copy()
    if selected_state:
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    if selected_zipcodes:
        filtered_df = filtered_df[filtered_df['ZIP Code'].isin(selected_zipcodes)]
    if selected_condition:
        filtered_df = filtered_df[filtered_df['Condition'] == selected_condition]
        
    fig = {
        'data': [
            {'x': filtered_df['Hospital Name'], 'y': filtered_df['Score'], 'type': 'bar'}
        ],
        'layout': {
            'title': 'Scores based on Zipcode, State, and Condition',
            'xaxis': {'title': 'Hospitals'},
            'yaxis': {'title': 'Score'}
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


