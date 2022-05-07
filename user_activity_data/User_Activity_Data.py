#!/usr/bin/env python3
import sys
import pandas as pd
import datetime
import os

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

app_dict = {}
ip_dict = {}
country_dict = {}

app_data = {"application_name": [], "total_hits": []}
country_data = {"country_name": [], "country_code": [], "total_hits": []}
user_data = {"user_id": [], "first_name": [], "last_name": [], "email": [], 
            "total_hits": []}


def init_df_dict(header: str, target_dict: dict, add_user_info=False) -> None:
    for i in range(1, 5):
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows():
            if pd.isna(row[header]):
                pass
            elif row[header] not in target_dict:
                target_dict[row[header]] = 1
            else:
                target_dict[row[header]] += 1




def parse_with_ip_data() -> None:
    df = pd.read_csv(parent_path + "/" + "csv_files/user_dataset.csv")
    lst = list(ip_dict.keys())
    print(lst)
    for index, row in df.iterrows():
        if str(row["ip_address"]) in lst:
            print("yui")
    


def main() -> None:
    """
    This program takes 2 command line args: 

    1. from_date
    2. to_date

    Creates 3 CSV files:
    1. top_3_applications.csv
    2. top_3_countries.csv
    3. top_10_users.csv
    """

    args = sys.argv[1:]

    if len(args) != 2:
        print("Usage: python3 User_Activity_Data.py from_date to_date")
        exit(1)

    init_df_dict("application", app_dict)  
    init_df_dict("source_ip", ip_dict)
    print(ip_dict)

    parse_with_ip_data()


    for i in range(0, 3):


        # Creates a dictionary to store top 3 applications 
        max_key_app = max(app_dict, key=app_dict.get)
        app_data["application_name"].append(max_key_app)
        app_data["total_hits"].append(app_dict[max_key_app])
        app_dict.pop(max_key_app)
    
    # This turns app_data into a pandas dataframe
    app_df = pd.DataFrame(app_data)  

    app_df.to_csv("top_3_applications_comp.csv", index=False)
    


if __name__ == "__main__":
    main()
