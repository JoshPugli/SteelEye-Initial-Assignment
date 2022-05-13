import pandas as pd
import datetime
import os

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))


def init_df_dict(header: str, target_dict: dict, date_lst: list) -> None:
    """Function that mutates target_dict parameter to store number of 
    occurances of each unique string under header. The keys represent
    unique strings at row with label "header" in activity_1-5.csv, 
    and the values are the total hits for each string.

    If date_lst != [None, None], this function will only count the 
    strings in rows containing to date cells larger than date_lst[0] and 
    smaller than date_lst[1].

    Note: If the date cell of a row is empty, it will be counted if the
    date_lst == [None, None], and will not be counted otherwise.
    """
    for i in range(1, 6):
        # Open each activity file 1-5 for reading
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows():
            
            # This will execute if user_main is run without args
            if date_lst[0] == None and date_lst[1] == None:
                if pd.isna(row[header]):
                    pass
                else:
                    if row[header] not in target_dict:
                        target_dict[row[header]] = 1
                    else:
                        target_dict[row[header]] += 1

            # If date_lst contains date objects
            else:
                
                # If header cell is empty, ignore
                if pd.isna(row[header]):
                    pass
                else:

                    if pd.isna(row["date"]):
                        pass
                    else:
                        # Convert date cell in current row to datetime df
                        input_date = row["date"].split("-")
                        row_date = datetime.datetime(int(input_date[0]), 
                                int(input_date[1]), int(input_date[2]))

                        # Either initialize or increment key-value pair
                        if date_lst[0] != None and date_lst[1] != None:
                            if row[header] in target_dict:
                                if row_date <= date_lst[1] and row_date >= date_lst[0]:
                                    target_dict[row[header]] += 1
                            else:
                                if row_date <= date_lst[1] and row_date >= date_lst[0]:
                                    target_dict[row[header]] = 1
                        elif date_lst[0] != None and date_lst[1] == None:
                            if row[header] in target_dict:
                                if row_date >= date_lst[0]:
                                    target_dict[row[header]] += 1
                            else:
                                if row_date >= date_lst[0]:
                                    target_dict[row[header]] = 1
                        else:
                            if row[header] in target_dict:
                                if row_date <= date_lst[1]:
                                    target_dict[row[header]] += 1
                            else:
                                if row_date <= date_lst[1]:
                                    target_dict[row[header]] = 1
