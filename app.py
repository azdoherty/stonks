import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from rotation import RotationChart


app = dash.Dash(__name__)


rchart = RotationChart()
rchart.download_starting_data()
rchart.process()


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
                        ) for c in [('RS-Ratio', 'IWM'), ('RS-Ratio', 'SPY')]
                    ]
            }
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
