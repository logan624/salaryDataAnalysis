# Import packages
from dash import Dash, html, dash_table, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


def main():
    # Incorporate data
    df = pd.read_csv('ds_salaries.csv')

    # Initialize the app
    app = Dash(
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # Create a Dash table to represent the dataframe
    dt = dash_table.DataTable(data=df.to_dict('records'),
                              page_size=10,
                              style_data_conditional=[
        # Set background color for odd rows
        {'if': {'row_index': 'odd'}, 'backgroundColor': 'lightgray'},
        # Set background color for even rows
        {'if': {'row_index': 'even'},
         'backgroundColor': 'white'},
        # Set text color for cells in 'Column 1' to red
        {'if': {'column_id': 'Column 1'}, 'color': 'red'},
        # Set text color for cells in 'Column 2' to blue
        {'if': {'column_id': 'Column 2'}, 'color': 'blue'},
        # Set background color to green and text color to white for cells in 'Column 1' with a value greater than 3
        {'if': {'filter_query': '{Column 1} > 3'},
         'backgroundColor': 'green', 'color': 'white'}
    ],
                              style_header_conditional=[
        {'if': {'column_editable': True}, 'backgroundColor': 'lightblue'},
        {'if': {'column_editable': False}, 'backgroundColor': 'lightgray'},
        {'if': {'column_id': 'Column 1'}, 'color': 'red'},
        {'if': {'column_id': 'Column 2'}, 'color': 'blue'}
    ]
    )

    # Create a bar chart figure to compare salary by experience
    salary_exp_bar = px.bar(df, x='experience_level',
                            y='salary_in_usd',
                            barmode='overlay',
                            color='remote_ratio',
                            labels={
                                "experience_level": "Experience Level",
                                "salary_in_usd": "Salary (USD)",
                                "remote_ratio": "Remote Ratio"
                            },
                            height=600,
                            opacity=1.0,
                            )
    salary_exp_bar.update_layout(
        paper_bgcolor='aquamarine', plot_bgcolor='lightgray')

    # Create a list of paragraph elements holding data about salary descriptive statistics
    salary_stats = getStatSummary(df['salary_in_usd'])
    salary_summary = [
        html.P(children=["Mean Salary        : $",
               "{:.2f}".format(salary_stats["mean"])]),
        html.P(children=["Median Salary      : $",
               "{:.2f}".format(salary_stats["median"])]),
        html.P(children=["Standard Deviation : $",
               "{:.2f}".format(salary_stats["std"])])
        # Leaving variance out for now-- not sure how valuable it is here
    ]

    # Create the app's layout
    app.layout = html.Div(
        style={'backgroundColor': 'lightblue', 'padding': '20px'},
        children=[
            html.Div(
                className="app-header",
                children=[
                    html.H1('Data Scientist Analysis')
                ]
            ),
            html.Div(
                children=html.Div([
                    html.H2('Dataframe Layout'),
                    dt
                ])
            ),
            html.Div(
                children=[
                    html.H2('Salary by Experience Level'),
                    dcc.Graph(id="graph", figure=salary_exp_bar)
                ]
            ),
            html.Div(
                children=[
                    html.H2('Salary Descriptive Statistics'),
                    *salary_summary
                ]
            )
        ])

    app.run_server(debug=True)


def getStatSummary(column):
    # Calculate the mean
    mean = (column.mean())
    # Calculate the median
    median = (column.median())
    # Calculate the standard deviation
    std = column.std()
    # Calculate the variance
    var = column.var()

    # Create a return object for the descriptive statistic values
    ret = {
        "mean": mean,
        "median": median,
        "std": std,
        "var": var
    }

    return ret


# Run the server
if __name__ == '__main__':
    main()
