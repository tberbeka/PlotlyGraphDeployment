# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import os



app = Dash(__name__)


current_path = os.getcwd()
files = os.listdir(current_path + '/Data/')
df = pd.DataFrame()
for file in files:
    temp = pd.read_csv(current_path + '/Data/'+ file)
    temp['file_name'] = file
    df = pd.concat([df,temp])
df[['city','type']] = df.file_name.str.split('_', expand = True)
df.type = df.type.str[:-4]
df = df.drop(columns = 'file_name')


df4 = pd.pivot_table(df, values = ['realSum','guest_satisfaction_overall'],index=['person_capacity','city'], aggfunc=np.mean)
df5=df4.reset_index()
df5.to_csv(file,index=False)
df6=pd.read_csv('vienna_weekends.csv')



app.layout = html.Div([
    html.H4('Animated AirBnB Prices'),
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='selection',
        options=["Bar","Scatter"],
        value='Bar',
    ),
    dcc.Loading(dcc.Graph(id="graph"), type="cube")
])


@app.callback(
    Output("graph", "figure"),
    Input("selection", "value"))


def display_animated_graph(selection):
    animations = {'Scatter': px.scatter(
            df6, x="guest_satisfaction_overall", y="realSum", animation_frame="person_capacity",
            animation_group="city", size='realSum', color="city",
            hover_name="realSum", size_max=50,
            range_x=[80,110], range_y=[0,2000]),

        'Bar': px.bar(
            df6, x="city", y="realSum",
            animation_frame="person_capacity", animation_group="city",
            range_y=[0,2000]),
    }
    return animations[selection]


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)

    # app.run_server(debug=False, host="0.0.0.0", port = 8080)