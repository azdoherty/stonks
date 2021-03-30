import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from rotation import RotationChart


app = dash.Dash(__name__)


rchart = RotationChart(
    start_date='2020-11-12',
    end_date='2021-03-12',
    tickers=['QQQ', 'XLE']
)
rchart.download_starting_data()
rchart.process()



chart_background = [
    go.Scatter(
        x=[97, 100, 100, 97, 97],
        y=[97, 97, 100, 100, 97],
        fill='toself',
        fillcolor='rgba(255, 235, 235, 255)',
        line=dict(color='rgba(255, 235, 235, 255)'),
    ),
    go.Scatter(
        x=[97, 100, 100, 97, 97],
        y=[100, 100, 103, 103, 100],
        fill='toself',
        fillcolor='rgba(235,235,255,255)',
        line=dict(color='rgba(235,235,255,255)'),
    ),
    go.Scatter(
        x=[100, 103, 103, 100, 100],
        y=[97, 97, 100, 100, 97],
        fill='toself',
        fillcolor='rgba(255,255,235,255)',
        line=dict(color='rgba(255,255,235,255)'),
    ),
    go.Scatter(
        x=[100, 103, 103, 100, 100],
        y=[100, 100, 103, 103, 100],
        fill='toself',
        fillcolor='rgba(235,245,235,255)',
        line=dict(color='rgba(235,245,235,255)'),
    )
]

app.layout = html.Div(
    children=[
        html.H1('Rotation Chart'),
        html.P(
            children='Rotation chart to analyze relative performance'
        ),
        dcc.Graph(
            figure={
                'data':
                    [
                        go.Scatter(
                            x=rchart.data.index,
                            y=rchart.data.loc[:, c],
                            mode="markers+lines",
                            name=c[1]
                        ) for c in [('RS-Ratio', 'XLE'), ('RS-Ratio', 'QQQ')]
                    ],

            }
        ),
        dcc.Graph(
            figure={
                'data':
                    chart_background + [
                        go.Scatter(
                            x=rchart.data.loc[:, ('JDK RS-ratio', c[1])],
                            y=rchart.data.loc[:, ('JDK RS-Momentum', c[1])],
                            hovertext=rchart.data.index,
                            mode="markers+lines",
                            name=c[1],
                        ) for c in [('RS-Ratio', 'XLE'), ('RS-Ratio', 'QQQ')]
                    ],
                'layout': dict(
                    height=800,
                    width=800
                )
            }

        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
