"""Plot a graph with the data

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.

"""

import random
import plotly.graph_objects as go
from date_definitions import get_date_string


def get_xy_data(article_scores: dict[tuple, float]) -> tuple[list[str], list[float]]:
    """Get the xy data from the dictionary of article scores"""
    x_data = []
    y_data = []
    for date in article_scores:
        x_data.append(get_date_string(date))
        y_data.append(article_scores[date])
    return (x_data, y_data)


def plot_data(genre: str, article_scores: dict[tuple, float]) -> None:
    """
    Plot the single percentage growth all genres with respect to time.

    """
    # Build the figure
    fig = go.Figure()
    # figure configuration
    x_data, y_data = get_xy_data(article_scores)
    fig.add_trace(go.Scatter(x=x_data,
                             y=y_data,
                             mode='lines',
                             name=genre,
                             marker=dict(color=f'rgb({random.randint(0, 255)}, '
                                               f'{random.randint(0, 255)}, '
                                               f'{random.randint(0, 255)})')))
    # display the figure in the html format
    fig.update_layout(title=f'Influence Score Growth of {genre}',
                      xaxis_title='(time)',
                      yaxis_title=f'(Calculated {genre} Influence Score)')
    fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
