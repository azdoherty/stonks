import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from rotation import RotationChart

app = dash.Dash(__name__)

# rchart = RotationChart()
# rchart.download_starting_data()
# rchart.normalize()

df = pd.DataFrame(
    [
        {
            'date': datetime(2021, 1, 1) + timedelta(days=i),
            'a': i,
            'b': i**2
        }
        for i in range(20)
    ]
)

df.set_index('date', inplace=True)

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
                            x=df.index,
                            y=df[i],
                            mode="markers+lines",
                        ) for i in ['a', 'b']
                    ]
            }
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
