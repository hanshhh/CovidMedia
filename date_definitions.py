"""
Some useful date manipulation definitions.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.

"""

START_DATE = (2020, 1, 1)
END_DATE = (2021, 12, 1)


def get_date_string(date: tuple[int, int, int]) -> str:
    """

    :param date: Date as (year, month, day)
    :return: String representing the date to send to the guardian API

    >>> get_date_string((2020, 1, 1))
    2020-01-01

    """
    year, month, day = date
    year, month, day = str(year), str(month), str(day)
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    return year + "-" + month + "-" + day


def next_date(date: tuple[int, int, int]) -> tuple[int, int, int]:
    """

    :param date: Starting date as (year, month, day)
    :return: Next date as (year, month, day)

    >>> next_date((2020, 1, 1))
    (2020, 1, 2)
    """

    num_days_per_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 1-indexed
    year, month, day = date
    if year % 4 == 0 and month == 2 and day == 28:
        return (year, 3, 1)
    if month == 12 and day == 31:
        return (year + 1, 1, 1)
    if day == num_days_per_month[month]:
        return (year, month + 1, 1)
    return (year, month, day + 1)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
