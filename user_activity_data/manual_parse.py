import pandas as pd
import os

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))


def parse_app_data(application: str, date: str) -> int:
    count = 0
    for i in range(1, 6):
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows(): 
            if row["application"] == application and row["date"] == date:
                count += 1
    
    return count

def parse_app_data_no_date(application: str) -> int:
    count = 0
    for i in range(1, 6):
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows(): 
            if row["application"] == application:
                count += 1
    
    return count

def main():
    count1 = parse_app_data("Safari", "2021-08-24")
    print(count1)
    count2 = parse_app_data_no_date("Safari")
    print(count2)

if __name__ == "__main__":
    main() 
