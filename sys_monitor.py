import dash
from dash.dependencies import Output, Input, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import psutil


cpu_usage = deque(maxlen=20)
mem_usage = deque(maxlen=20)
disk_usage = deque(maxlen=20)
X = deque(maxlen=20)

X.append(1)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000
        )
    ]
)

@app.callback(Output('live-graph', 'figure'),
                     events= [Event('graph-update', 'interval')])
def update_graph():

    cpu_percent = int(psutil.cpu_percent())
    mem_percent = int(psutil.virtual_memory().percent)
    disk_percent = int(psutil.disk_usage("C:\\").percent)
    
    cpu_usage.append(cpu_percent)
    mem_usage.append(mem_percent)
    disk_usage.append(disk_percent)
    X.append(X[-1] + 1)

    cpu_data = go.Scatter(
        x = list(X),
        y = list(cpu_usage),
        name = 'CPU',
        mode = 'lines',
    )

    mem_data = go.Scatter(
        x = list(X),
        y = list(mem_usage),
        name = 'RAM',
        mode = 'lines',
    )

    disk_data = go.Scatter(
        x = list(X),
        y = list(disk_usage),
        name = 'Schijf',
        mode = 'lines',
    )

    return {
        'data': [cpu_data, mem_data, disk_data],
        'layout': go.Layout(title='Systeem monitor', 
                            xaxis=dict(range=[min(X), max(X)]),
                            yaxis=dict(range=[0, 101]))
    }

if __name__ == '__main__':
    app.run_server(debug=True)
