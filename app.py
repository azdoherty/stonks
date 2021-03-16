import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from rotation import RotationChart

app = dash.Dash(__name__)

#
# rchart = RotationChart()
# rchart.download_starting_data()
# rchart.normalize()

df = pd.DataFrame(
    [
        {
            'a': i,
            'b': i**2
        }
        for i in range(20)
    ]
)


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
                        {
                            'x': df.index,
                            'y': df['a']
                        }
                    ]
            }
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
