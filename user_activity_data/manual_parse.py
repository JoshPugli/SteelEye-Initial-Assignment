import pandas as pd
import os
import ipaddress

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

country_data = {"country_name": [], "country_code": [], "total_hits": []}
user_data = {"user_id": [], "first_name": [], "last_name": [], "email": [], 
            "total_hits": []}

def parse_app_data(application: str, date: str) -> int:
    count = 0
    for i in range(1, 6):
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows(): 
            if row["application"] == application and row["date"] == date:
                count += 1

    return count

    # df = pd.read_csv(parent_path + "/" + "csv_files/user_dataset.csv")
    # for index, row in df.iterrows():
    #     if pd.notna(row["ip_address"]):
    #         if ipaddress.ip_address(row["ip_address"]) in ipaddress.ip_network('177.145.0.0/16'):
    #                 print("yuh")
