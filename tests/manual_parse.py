import pandas as pd
import os

from os.path import dirname, realpath

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))


def parse_app_data(application: str, date: str) -> int:
    """Naive way to count actions for a particular application on a 
    particular day. Used exclusively to test user_activity_main.py.
    """
    count = 0
    for i in range(1, 6):
        df = pd.read_csv("../csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows(): 
            if row["application"] == application and row["date"] == date:
                count += 1
    
    return count


def parse_app_data_no_date(application: str) -> int:
    """Naive way to count actions for a particular application. Used 
    exclusively to test user_activity_main.py.
    """
    count = 0
    for i in range(1, 6):
        df = pd.read_csv("../csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows(): 
            if row["application"] == application:
                count += 1
    
    return count


def main():
    count1 = parse_app_data("Safari", "2021-08-24")
    count2 = parse_app_data_no_date("Safari")


if __name__ == "__main__":
    main() 


# git push https://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@github.com/JoshPugli/SteelEye-Initial-Assignment.git
