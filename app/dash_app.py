from dash import Dash, html
import plotly.graph_objs as go


from measurements import (
    update_msts,
    cpu,
    CPU_COUNT,
    ram,
    cpu_qnt,
    pc_info,
    cpu_freq,
    memory,
    disk_info,
    disks,
    net_stat,
    sent_packs
)

dash_app = Dash(__name__, requests_pathname_prefix="/dash/", title="System online")

dash_app.layout = html.H1("demo page")

from dash import Dash, dcc, callback, Input, Output, html
import plotly


external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]

dash_app.layout = html.Div(
    [
        html.P(id="cpu-usage-text", className="text-2xl font-pipboy text-green-500"),
        html.Div(children=pc_info, style={'fontFamily': 'Terminal, monospace', 'color': 'orange', 'fontSize': '20px'}),
        #html.Div(children=cpu_freq),
        #html.Div(children=cpu_qnt),
        dcc.Graph(id="cpu_graph"),
        #html.Div(children=memory),
        dcc.Graph(id="ram_swap"),
        html.Div(children=disk_info),
        dcc.Graph(id="disks"),
        #html.Div(children=sent_packs),
        dcc.Graph(id="net_stat"),
        dcc.Interval(id="timer", interval=100),
    ]
)


@callback(
    Output("cpu_graph", "figure"),
    Output("ram_swap", "figure"),
    Output("disks", "figure"),
    Output("net_stat", "figure"),
    Input("timer", "n_intervals"),
)
def update(n):
    update_msts()

    cpu_traces = []
    for i in range(CPU_COUNT):

        cpu_traces.append(
            go.Scatter(x=list(range(250)), y=cpu[i], name=f"CPU{i}", line=dict(color="#f7dc6f", width=2), mode="lines+markers")
        )

    ram_traces = [
        go.Scatter(x=list(range(250)), y=ram[0], name=f"ram", line=dict(color="#00ff00", width=2), mode="lines+markers"),
        go.Scatter(x=list(range(250)), y=ram[1], name=f"swap", line=dict(color="#0080ff", width=2), mode="lines+markers"),
    ]

    disks_traces = [
        go.Scatter(x=list(range(250)), y=disks[0], name=f"disk_read", line=dict(color="#ffa500", width=2), mode="lines+markers"),
        go.Scatter(x=list(range(250)), y=disks[1], name=f"disk_write", line=dict(color="#ff0000", width=2), mode="lines+markers"),
    ]

    net_traces = [
        go.Scatter(x=list(range(250)), y=net_stat[0], name=f"net_sent", line=dict(color="#ffff00", width=2), mode="lines+markers"),
        go.Scatter(x=list(range(250)), y=net_stat[1], name=f"net_recv", line=dict(color="#00ffff", width=2), mode="lines+markers"),
    ]

    layout = dict(
        title="System Monitor",
        titlefont=dict(family="Courier New, monospace", size=24, color="#ffffff"),
        xaxis=dict(title="Time", titlefont=dict(family="Courier New, monospace", size=18, color="#ffffff"), tickfont=dict(family="Courier New, monospace", size=14, color="#ffffff")),
        yaxis=dict(title="Usage", titlefont=dict(family="Courier New, monospace", size=18, color="#ffffff"), tickfont=dict(family="Courier New, monospace", size=14, color="#ffffff")),
        plot_bgcolor="#2b2b2b",
        paper_bgcolor="#2b2b2b",
        font=dict(family="Courier New, monospace", size=14, color="#ffffff"),
        legend=dict(font=dict(family="Courier New, monospace", size=14, color="#ffffff"), orientation="h"),
        margin=dict(l=50, r=50, t=50, b=50),
    )

    return dict(data=cpu_traces, layout=layout), dict(data=ram_traces, layout=layout), dict(data=disks_traces, layout=layout), dict(data=net_traces, layout=layout)
