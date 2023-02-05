from typing import Dict, Optional

import pandas as pd
from plotly import graph_objs as go


def get_line_plot(
        df: pd.DataFrame,
        xaxis_value_name: str,
        yaxis_value_names: Dict[str, str],
        title: Optional[str] = None
):
    fig = go.Figure()
    for y, yname in yaxis_value_names.items():
        fig.add_trace(go.Scatter(x=df[xaxis_value_name], y=df[y], name=yname))
    fig.layout.update(title_text=title)
    return fig


def get_time_series_plot(
        df: pd.DataFrame,
        xaxis_value_name: str,
        yaxis_value_names: Dict[str, str],
        title: Optional[str] = None,
        include_range_slider: bool = False,
):
    fig = get_line_plot(df, xaxis_value_name, yaxis_value_names, title)

    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        height=450,
        plot_bgcolor="rgba(0,0,0,0)"
    )
    fig.update_xaxes(
        showline=True,
        showgrid=False, 
        linecolor='white',
        rangeslider_visible=True,
        # xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all", label="Since Inception"),
                ]
            ),
            # font=list([dict(color="blue")])
        ),
        # rangeslider=dict(visible=include_range_slider),
        type="date",
    )
    fig.update_yaxes(showgrid=True, 
                     gridcolor="rgb(220,220,220)",
                     nticks=5, 
                     griddash="dot")
    fig.update_traces(marker_color="rgb(0,38,100)")
    fig.update_layout(xaxis_rangeselector_activecolor='darkslategrey',
                      xaxis_rangeselector_font_color='black',
                      xaxis_rangeselector_bgcolor='grey'
                      )

# )
    return fig


def get_pie_chart(
        df: pd.DataFrame,
        label_col: str,
        values_col: str,
        title: Optional[str] = None
):
    labels = df[label_col].to_list()
    values = df[values_col].to_list()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title=title)
    return fig
