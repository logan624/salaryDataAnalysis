# Import packages
from dash import Dash, html, dash_table, dcc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Incorporate data
df = pd.read_csv('ds_salaries.csv')

# Initialize the app
app = Dash(__name__)

# Create a bar chart figure to compare salary by experience
fig = px.bar(df, x='experience_level',
                 y='salary_in_usd',
                 barmode='overlay',
                 labels = {
                            "experience_level" : "Experience Level",
                            "salary_in_usd" : "Salary (USD)"
                 },
                 height = 600,
                 opacity = 1.0
            )

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.H1('Data Scientist Analysis')
        ]
    ),
    html.Div(
        children=html.Div([
            html.H2('Dataframe Layout'),
            dash_table.DataTable(data=df.to_dict('records'), page_size=10)
        ])
    ),
    html.Div(
        children=[
            html.H2('Salary by Experience Level'),
            dcc.Graph(id="graph", figure=fig)
        ]
    ),
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
