import sys
import os
import unittest
import manual_parse
import pandas as pd

sys.path.append(os.path.abspath('../user_activity_data'))

import user_activity_main

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

class TestActivity(unittest.TestCase):
    """Testing takes a long time, but each test is comprehensive"""

    def test_single_day(self):
        """Test user_activity_main for each individual day in August 2021"""
        for i in range(1, 32):
            user_activity_main.run_program(i, i)
            df = pd.read_csv("top_3_applications.csv")
            
            if i < 10:
                day = "2021-08-0" + str(i)
            else:
                day = "2021-08-" + str(i)
            
            for index, row in df.iterrows(): 
                count = manual_parse.parse_app_data(row["application_name"], 
                    day)
                assert(count == row["total_hits"])


    def test_no_args(self):
        """Test user_activity_main when no args are passed in"""
        user_activity_main.run_program()
        df = pd.read_csv("top_3_applications.csv")
        for index, row in df.iterrows(): 
            count = manual_parse.parse_app_data_no_date(row["application_name"])
            assert(count == row["total_hits"])
        

if __name__ == '__main__':
    unittest.main()