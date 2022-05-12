from pseudo_header import path, parent_path, init_df_dict
import pandas as pd
from ipwhois import IPWhois


# Initializes input dates. This is mutated by user input through main.py
input_dates = [None, None]

def main():
    """ Work in progress...

    Currently using whois data to find ip ranges. Will add more later.
    """

    ip_dict = {}
    
    init_df_dict("source_ip", ip_dict, input_dates)

    cidr_lst = []
    range_lst = []
    for key in ip_dict:
        obj = IPWhois(key)
        results = obj.lookup_whois()

        cidr = results["nets"][0]["cidr"]
        range = results["nets"][0]["range"]
        cidr_lst.append(cidr)
        range_lst.append(range)
    
        # ipaddress.ip_address('192.168.0.1') in ipaddress.ip_network('192.168.0.0/24')
    
    df = pd.read_csv(parent_path + "/" + "csv_files/user_dataset.csv")

    print(range_lst)

    

