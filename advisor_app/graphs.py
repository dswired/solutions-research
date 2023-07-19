from typing import Dict, Optional, Union

import pandas as pd
from plotly import graph_objs as go


def get_line_plot(
    df: pd.DataFrame,
    xaxis_value_name: str,
    yaxis_value_names: Dict[str, str],
    title: Optional[str] = None,
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
        xaxis=dict(
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
                )
            ),
            rangeslider=dict(visible=include_range_slider),
            type="date",
        )
    )
    return fig


def get_pie_chart(
    df: pd.DataFrame, label_col: str, values_col: str, title: Optional[str] = None
):
    labels = df[label_col].to_list()
    values = df[values_col].to_list()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title=title)
    return fig


def get_bar_chart(
    df: pd.DataFrame, label_col: str, values_cols: list, title: Optional[str] = None
):
    data = [go.Bar(name=col, x=df[label_col], y=df[col]) for col in values_cols]
    fig = go.Figure(data=data)
    fig.update_layout(title=title)
    return fig


def get_scatter(df: pd.DataFrame, x_col: str, y_col: str, color: str = None):
    ...
