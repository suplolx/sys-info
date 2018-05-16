import dash
from dash.dependencies import Output, Input, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import psutil


bytes_recv = deque(maxlen=20)
megabyte_per_second = deque(maxlen=20)
X = deque(maxlen=20)

X.append(1)
bytes_recv.append(psutil.net_io_counters().bytes_recv)

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
    bytes_recv_start = psutil.net_io_counters().bytes_recv
    bytes_per_second = bytes_recv_start - bytes_recv[-1]
    bytes_recv.append(bytes_recv_start)
    megabyte_per_second.append(round(bytes_per_second / 2**20, 2))
    X.append(X[-1] + 1)

    net_data = go.Scatter(
        x = list(X),
        y = list(megabyte_per_second),
        name = 'CPU',
        mode = 'lines',
    )

    return {
        'data': [net_data],
        'layout': go.Layout(title='Download speed', 
                            xaxis=dict(range=[min(X), max(X)]),
                            yaxis=dict(range=[0, max(megabyte_per_second) + 2]))
    }

if __name__ == '__main__':
    app.run_server(debug=True)
