"""Prepares processed data for the graphs

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.
"""

import csv
from Article import Article
from date_definitions import get_date_string, next_date, END_DATE
from plotdata import plot_data

genres = {'other': {'search', 'about', 'info', 'help', 'culture-professionals-network',
                    'enterprise-network', 'culture-network',
                    'global-development-professionals-network', 'government-computing-network',
                    'higher-education-network', 'healthcare-network', 'housing-network',
                    'social-enterprise-network', 'small-business-network', 'social-care-network',
                    'public-leaders-network', 'teacher-network', 'voluntary-sector-network',
                    'local-government-network', 'media-network', 'extra', 'theguardian',
                    'community', 'society-professionals', 'guardian-professional',
                    'working-in-development', 'animals-farmed', 'crosswords'},
          'news': {'news', 'tv-and-radio', 'theobserver', 'media', 'commentisfree', 'membership'},
          'culture': {'culture', 'artanddesign', 'books', 'childrens-books-site', 'music',
                      'food', 'film', 'fashion', 'stage', 'lifeandstyle', 'sport', 'football',
                      'games', 'education'},
          'politics and global news': {'politics', 'inequality', 'law', 'women-in-leadership',
                                       'world', 'travel', 'travel/offers', 'australia-news',
                                       'uk-news', 'us-news', 'society', 'global-development',
                                       'katine', 'cities', 'weather', 'local', 'leeds', 'edinburgh',
                                       'cardiff', 'environment'},
          'science and technology': {'science', 'technology'},
          'business': {'better-business', 'business', 'business-to-business',
                       'money', 'jobsadvice'},
          'all': set()}


def load_articles() -> dict[tuple, list[Article]]:
    """
    :return: A dictionary mapping each date as a tuple of (year, month, day)
    to a list of articles that were published on that day.
    """

    curr_date = (2020, 1, 1)
    article_dict = {}
    while curr_date != END_DATE:
        with open('./processed_data/' + get_date_string(curr_date) + '.csv', 'r', encoding='utf-8') as readfile:
            reader = csv.reader(readfile, delimiter=',')
            article_dict[curr_date] = []
            for row in reader:
                if len(row) == 0:
                    continue
                article_dict[curr_date].append(Article(curr_date, row[1], row[2], float(row[3])))
        curr_date = next_date(curr_date)
    return article_dict


def average_influence_day(articles: list[Article], sections: set[str]) -> float:
    """Returns the average of all the influence scores of the given articles

    >>> average_influence_day([Article((2020, 3, 1), 'horror', 'horror', 5)], {'horror'})
    5.0
    """
    articles = filter_genres(articles, sections)

    tot_so_far = 0
    if len(articles) == 0:
        return 0
    for article in articles:
        tot_so_far += article.influence_score

    return tot_so_far / len(articles)


def filter_genres(articles: list[Article], sections: set[str]) -> list[Article]:
    """Returns a list of Articles with one of the given section sections

    >>> x = filter_genres([Article((2020, 3, 1), 'horror', 'horror', 5), \
    Article((2020, 3, 2), 'mystery', 'mystery', 1)], {'horror'})
    >>> len(x) == 1
    True
    """
    if sections == set():
        return articles
    filtered_articles = []
    for article in articles:
        if article.section_id in sections:
            filtered_articles.append(article)
    return filtered_articles


def get_plot_data(articles: dict[tuple: list[Article]], sections: set[str],
                  start_date: tuple[int, int, int]) -> dict[tuple[int, int, int], float]:
    """Returns a dictionary mapping dates in the range to the influence score of articles on that
    day, from start_date to END_DATE.

    >>> get_plot_data({(2020, 3, 1): [Article((2020, 3, 1), 'horror', 'horror', 5)]}, {'horror'})
    {(2020, 3, 1): 5.0}
    """
    day_to_score = {}
    curr_date = start_date
    while curr_date != END_DATE:
        day_to_score[curr_date] = average_influence_day(articles[curr_date], sections)
        curr_date = next_date(curr_date)
    return day_to_score


def display_graph(current_settings: tuple[int, int], articles: dict[tuple, list[Article]]) -> None:
    """Display the graph of the current settings and all articles

    current_settings is (section, duration) in integer forms
    """
    # use settings to get plot data, then return the graph from plotdata.py
    sections = ['all', 'science and technology', 'business', 'politics and global news',
                'news', 'culture', 'other']
    dates = [(2020, 1, 1), (2021, 6, 1), (2021, 11, 1), (2021, 11, 24)]

    genre = sections[current_settings[0]]
    start_date = dates[current_settings[1]]
    plot_data(genre, get_plot_data(articles, genres[genre], start_date))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
