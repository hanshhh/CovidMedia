"""
Main function

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Brian Wang, Yahya Elgabra, Kareem Salem, Wenqi Zhan.

"""
from gui import main_loop

# Uncomment lines 20-23 to get data from api and preprocess it
# Be warned that pulling the API will take approximately 30 minutes due to rate limiting.
# from api_pull import pull_from_api
# from preprocess_raw_data import process_raw_data
# pull_from_api((2020, 1, 1))
# process_raw_data((2020, 1, 1))

main_loop()
