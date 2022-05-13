import unittest
import user_activity_main
import manual_parse
import pandas as pd

class TestActivity(unittest.TestCase):

    def test_single_day(self):
        for i in range(1, 32):
            user_activity_main.run_program(i, i)
            df = pd.read_csv("top_3_applications.csv")
            
            if i < 10:
                day = "2021-08-0" + str(i)
            else:
                day = "2021-08-" + str(i)
            
            for index, row in df.iterrows(): 
                count = manual_parse.parse_app_data(row["application_name"], day)
                assert(count == row["total_hits"])


    def test_no_args(self):
        user_activity_main.run_program()
        df = pd.read_csv("top_3_applications.csv")
        for index, row in df.iterrows(): 
            count = manual_parse.parse_app_data_no_date(row["application_name"])
            assert(count == row["total_hits"])
        
    

if __name__ == '__main__':
    unittest.main()