from pseudo_header import path, parent_path, init_df_dict
import pandas as pd

# Initializes input dates. This is mutated by user input through main.py
input_dates = [None, None]

def main():

    ip_dict = {}
    
    init_df_dict("source_ip", ip_dict, input_dates)
    