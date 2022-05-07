import pandas as pd
from pseudo_header import path, parent_path, init_df_dict

input_dates = [None, None]

def main():

    app_dict = {}
    app_data = {"application_name": [], "total_hits": []}
    
    init_df_dict("application", app_dict, input_dates)  

    print(app_dict)

    for i in range(0, 3):

        # Creates a dictionary to store top 3 applications 
        max_key_app = max(app_dict, key=app_dict.get)
        app_data["application_name"].append(max_key_app)
        app_data["total_hits"].append(app_dict[max_key_app])
        app_dict.pop(max_key_app)
        
    # This turns app_data into a pandas dataframe
    app_df = pd.DataFrame(app_data)  
    print(app_df)
    app_df.to_csv("top_3_applications.csv", index=False)