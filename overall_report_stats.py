"""
Overall report statistics.
"""

from process_data import filter_genres, genres, average_influence_day
from Article import Article


def get_overall_statistics(articles: dict[tuple, list[Article]]) -> dict[str, tuple[int, float, int]]:
    """
    Returns the number of articles, average influence score,
    and number of articles above a threshold score of 3.5 for each genre.
    """
    article_list = []
    for date in articles:
        article_list.extend(articles[date])

    stats = {}
    for genre in genres:
        num_articles = len(filter_genres(article_list, genres[genre]))
        avg_score = average_influence_day(article_list, genres[genre])
        num_influenced = sum(
            [article.influence_score >= 3.5 for article in filter_genres(article_list, genres[genre])])
        stats[genre] = (num_articles, avg_score, num_influenced)
    return stats


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
