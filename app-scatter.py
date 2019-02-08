import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# prep data for use in scatter graph
df = pd.read_csv("https://raw.githubusercontent.com/annajgibson/dash-hackney-pop/master/ward_housing_led_2016_base_hackney.csv")
df = df[['gss_code_borough', 'gss_code_ward', 'district', 'ward_name', 'age', '2015', '2020', '2025', '2030', '2035', '2040', '2045', '2050']]
df['id'] = df.index
df = df.melt(id_vars=['id', 'gss_code_borough', 'gss_code_ward', 'district', 'ward_name', 'age'], value_vars=['2015', '2020', '2025', '2030', '2035', '2040', '2045', '2050'])
df = df.rename(columns={'variable': 'year', 'value':'pop'})
df = df.loc[df['age']!='total'] #remove total rows
df['year'] = df.year.astype(int) 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Dash example'),
    dcc.Graph(id='graph-with-slider'
    ),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
    
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    print(selected_year)
    traces = []
    for i in filtered_df.ward_name.unique():
        df_by_area = filtered_df[filtered_df['ward_name'] == i]
        traces.append(go.Scatter(
            x=df_by_area['age'],
            y=df_by_area['pop'],
            text=df_by_area['ward_name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 8,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {'data': traces,
        'layout': go.Layout(
            title='Projected Population by Ward',
            xaxis={'title': 'Age', 'range': [0, 100]},
            yaxis={'title': 'Population', 'range': [0, 1000]},
            margin={'l': 60, 'b': 60, 't': 60, 'r': 60},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)