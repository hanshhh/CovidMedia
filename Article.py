"""
Class Article.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.
"""


class Article:
    """A news article.

    Instance Attributes:
      - date: Date the article was published as (year, month, day)
      - section_id: Id of the section of the article as given by the guardian API
      - section_name: Name of the section of the article as given by the guardian API
      - influence_score: Relevance of the article to COVID as calculated by an algorithm

    """
    date: tuple[int, int, int]
    section_id: str
    section_name: str
    influence_score: float

    def __init__(self, date: tuple[int, int, int],
                 section_id: str, section_name: str,
                 influence_score: float) -> None:
        self.date = date
        self.section_id = section_id
        self.section_name = section_name
        self.influence_score = influence_score


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
