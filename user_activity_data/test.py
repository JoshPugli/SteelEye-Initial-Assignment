import unittest
import user_activity_main
import manual_parse
import pandas as pd

class TestActivity(unittest.TestCase):

    def test_no_args(self):
        user_activity_main.main()
        df = pd.read_csv("top_3_applications.csv")

        
    

if __name__ == '__main__':
    unittest.main()