import pandas as pd
from pseudo_header import init_df_dict

# Initializes input dates. This is mutated by user input through 
# user_activity_main.py
input_dates = [None, None]

def main():
    """ Calls init_df_dict from pseudo_header.py to create a dictionary 
    conatining the applications (from all activity csv files) as keys, and 
    the number of times they appear as values.

    Takes the applications with the highest 3 values, and uses pandas library
    to create the csv file "top_3_applications.csv" that contains the total 
    hits and application name for each of the top 3 applications.
    """

    # Parameter to init_df_dict
    app_dict = {}
    # Will store top 3 applications, and their corresponding hits
    app_data = {"application_name": [], "total_hits": []}
    
    init_df_dict("application", app_dict, input_dates)  

    for i in range(0, 3):

        # Creates a dictionary to store top 3 applications 
        try:
            max_key_app = max(app_dict, key=app_dict.get)
            app_data["application_name"].append(max_key_app)
            app_data["total_hits"].append(app_dict[max_key_app])
            app_dict.pop(max_key_app)
        except ValueError:
            pass
    
    # In the case where there is no activity in the provided range
    if app_data == {"application_name": [], "total_hits": []}:
        app_data = {"application_name": ["Safari", "Microsoft Edge", 
            "Internet Explorer"], "total_hits": [0, 0, 0]}

    # Turn app_data into a pandas dataframe, and convert to csv file
    app_df = pd.DataFrame(app_data)  
    app_df.to_csv("top_3_applications.csv", index=False)