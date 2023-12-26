"""
Get data from the guardian API and store it in a file for use.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.

"""

import requests
import csv
import time
from date_definitions import get_date_string, next_date, END_DATE
from bs4 import BeautifulSoup
import os

PAGE_SIZE = 200


def pull_from_api(curr_date: tuple[int, int, int]) -> None:
    """
    Pulls article data from the API.
    :param curr_date: The starting date to pull data from
    :return: Nothing
    """
    # automatically create the raw_data folder if it does not exist
    if not os.path.exists('./raw_data'):
        os.makedirs('./raw_data')

    num_pulls = 0  # rate limit of 5k pulls per day
    # this loop iterates through every single day, and makes sure we do not exceed rate limit
    while num_pulls < 5000 and curr_date != END_DATE:

        # open a file to write data to
        with open('./raw_data/' + get_date_string(curr_date) + '.csv', 'w', encoding="utf-8") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

            # api shows a maximum of PAGE_SIZE results per page, so we need one pull for every page.
            current_page = 1

            # once again make sure we do not exceed rate limit, we leave the loop using break statements
            while num_pulls < 5000:
                num_pulls += 1
                query = get_params(curr_date, current_page)
                request = requests.get("https://content.guardianapis.com/search", params=query)
                response = request.json().get("response")
                if response.get('status') != "ok":
                    print(response)
                    num_pulls = 5000
                    break

                results = response.get("results")

                for article in results:
                    # use beautifulsoup to strip html tags for each article.
                    soup = BeautifulSoup(article.get('fields').get('body').encode('ascii', 'ignore').decode())
                    bodytext = soup.get_text()
                    wr.writerow([
                        article.get('webPublicationDate'),
                        article.get('sectionId'),
                        article.get('sectionName'),
                        # article.get('type'),
                        article.get('webUrl'),
                        # article.get('webTitle'),
                        article.get('fields').get('headline'),
                        bodytext,
                        article.get('fields').get('wordcount')
                    ])
                current_page += 1
                if current_page > response.get('pages'):
                    break
                time.sleep(0.1)  # delay for ratelimiting
        curr_date = next_date(curr_date)


def get_params(date: tuple[int, int, int], current_page: int):
    """
    Get the query parameters for an api request with the given date and page.
    :param date: The date to search articles for
    :param current_page: Page number to get requests for
    :return: a dictionary of query parameters
    """
    query_params = {
        "api-key": "219f5695-c8e7-40f4-b0ac-0da0f294b965",
        "page": current_page,
        "show-fields": "headline,wordcount,body",
        "page-size": PAGE_SIZE,
        "lang": "en",
        "from-date": get_date_string(date),
        "to-date": get_date_string(date)
    }
    return query_params


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
