"""
Preprocess raw data in order to reduce file size.

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
import math
import os
from date_definitions import next_date, get_date_string, END_DATE
csv.field_size_limit(1000000)


def process_raw_data(curr_date: tuple[int, int, int]) -> None:
    """
    Prerequisites: the raw_data folder exists and all the files are in the required syntax

    :param curr_date: The starting date to pull data from
    :return: Nothing
    """
    # make the processed_data folder if it does not exist
    if not os.path.exists('./processed_data'):
        os.makedirs('./processed_data')

    while curr_date != END_DATE:
        with open('./raw_data/' + get_date_string(curr_date) + '.csv', 'r', encoding='utf-8') as readfile:
            with open('./processed_data/' + get_date_string(curr_date) + '.csv', 'w', encoding="utf-8") as writefile:
                reader = csv.reader(readfile, delimiter=',')
                writer = csv.writer(writefile, quoting=csv.QUOTE_ALL)
                for row in reader:
                    if len(row) == 0:
                        continue
                    writer.writerow([
                        row[0],
                        row[1],
                        row[2],
                        calc_influence_score(row[3], row[4], int(row[5]))
                    ])
        curr_date = next_date(curr_date)


# dictionary mapping key words to their weight

keys = {'covid': 3.0, 'abstinence': 2.0, 'acute': 2.0, 'adhere': 1.0, 'adherence': 1.0,
        'adverse': 1.0, 'biology': 3.0, 'biological': 3.0, 'anxiety': 3.0, 'mental': 3.0,
        'health': 3.0, 'assess': 1.0, 'bacteria': 3.0, 'burden': 1.0, 'capacity': 2.0,
        'carcinogen': 3.0, 'case': 2.0, 'cases': 2.0, 'study': 1.0, 'studies': 1.0, 'report': 1.0,
        'chronic': 3.0, 'illness': 3.0, 'ill': 3.0, 'condition': 2.0, 'contact': 2.0,
        'contagious': 3.0, 'contamination': 3.0, 'contaminate': 3.0, 'data': 1.0, 'disease': 3.0,
        'detect': 1.0, 'distribution': 2.0, 'dose': 3.0, 'effect': 1.0, 'effectiveness': 1.0,
        'efficacy': 3.0, 'efficiency': 1.0, 'ensure': 1.0, 'epidemiology': 3.0, 'exposure': 2.0,
        'exposed': 1.0, 'feasible': 1.0, 'global': 1.0, 'corona': 3.0, 'coronavirus': 3.0,
        'novel': 1.0, 'glucose': 3.0, 'guidelines': 3.0, 'vaccine': 3.0, 'vaccines': 3.0,
        'rollout': 3.0, 'care': 2.0, 'public': 2.0, 'disabled': 2.0, 'factor': 1.0, 'wheezing': 3.0,
        'astrazeneca': 3.0, 'optimal': 1.0, 'lungs': 2.0, 'moderna': 3.0, 'utilize': 1.0,
        'individuals': 1.0, 'methods': 1.0, 'persons': 1.0, 'screen': 2.0, 'individual': 1.0,
        'infectious': 3.0, 'impact': 1.0, 'hospitalization': 3.0, 'impaired': 2.0, 'diseases': 3.0,
        'sanitize': 3.0, 'cdc': 3.0, 'severe': 2.0, 'sneeze': 2.0, 'prevalence': 1.0,
        'provider': 1.0, 'morbid': 2.0, 'biontech': 3.0, 'outcome': 1.0, 'heart': 2.0,
        'assessment': 1.0, 'medication': 3.0, 'morbidity': 3.0, 'surgery': 3.0, 'toxic': 1.0,
        'period': 1.0, 'sinopharm': 3.0, 'monitor': 1.0, 'intake': 1.0, 'incubation': 1.0,
        'private': 1.0, 'transmit': 3.0, 'intervention': 2.0, 'respiratory': 3.0, 'hazardous': 1.0,
        'prolonged': 1.0, ' prevalent': 1.0, 'wipes': 1.0, 'preventable': 1.0, 'immunization': 3.0,
        'range': 1.0, 'immune': 3.0, 'pfizer': 3.0, 'infection': 3.0, 'vaccinated': 3.0,
        'reduce': 1.0, 'virus': 3.0, 'incidence': 1.0, 'long-term': 2.0, 'host': 2.0, 'clean': 2.0,
        'permissible': 3.0, 'initiative': 1.0, 'wheeze': 3.0, 'home': 1.0, 'sustain': 2.0,
        'medical': 3.0, 'distancing': 3.0, 'lockdown': 3.0, 'johnson': 3.0, 'endemic': 3.0,
        'symptoms': 3.0, 'rate': 2.0, 'social': 2.0, 'screening': 3.0, 'surveillance': 1.0,
        'population': 2.0, 'medicine': 3.0, 'referral': 1.0, 'risk': 2.0, 'pandemic': 3.0,
        'janssen': 3.0, 'vaccination': 3.0, 'toxicity': 2.0, 'disabilities': 2.0, 'localized': 2.0,
        'person': 1.0, 'transmission': 3.0, 'disparities': 1.0, 'epidemic': 3.0, 'response': 1.0,
        'disables': 3.0, 'hospitalisation': 3.0, 'sanitise': 3.0, 'nhs': 3.0,
        'headache': 3.0, 'tiredness': 3.0, 'stress': 3.0, 'quarantine': 3.0}


def calc_influence_score(headline: str, body: str, word_count: int) -> float:
    """Returns a float representing how influenced the article is by public health, soft-capped
    by the logarithmic function

    >>> calc_influence_score('COVID', 'the coronavirus is killing everybody', 6)
    5.711065366376011
    """

    filtered_headline = headline.lower().split()
    filtered_body = body.lower().split()
    score = 0

    weight = 10  # weight of words in headline relative to body

    for word in filtered_headline:
        if word in keys:
            score += keys[word] * weight

    for word in filtered_body:
        if word in keys:
            score += keys[word]

    return math.log(1 + score / (1 + (word_count / 1000)))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
