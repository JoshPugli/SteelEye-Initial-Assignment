import pandas as pd
import datetime
import os

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))


def init_df_dict(header: str, target_dict: dict, date_lst: list) -> None:
    print(date_lst[0])
    print(date_lst[1])
    for i in range(1, 6):
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows():
            
            if date_lst[0] == None and date_lst[1] == None:
                if row[header] not in target_dict:
                    target_dict[row[header]] = 1
                else:
                    target_dict[row[header]] += 1
            else:

                if pd.isna(row[header]):
                    pass
                else:

                    # Get date from current row
                    if pd.isna(row["date"]):
                        pass
                    else:
                        input_date = row["date"].split("-")
                        row_date = datetime.datetime(int(input_date[0]), 
                                int(input_date[1]), int(input_date[2]))


                        if row[header] not in target_dict:
                            if date_lst[0] != None and date_lst[1] == None:
                                if row_date >= date_lst[0]:
                                    target_dict[row[header]] = 1
                            elif date_lst[0] == None and date_lst[1] != None:
                                if row_date <= date_lst[1]:
                                    target_dict[row[header]] = 1
                            else:
                                if row_date <= date_lst[1] and row_date >= date_lst[0]:
                                    target_dict[row[header]] = 1
                        else:
                            if date_lst[0] != None and date_lst[1] == None:
                                if row_date >= date_lst[0]:
                                    target_dict[row[header]] += 1
                            elif date_lst[0] == None and date_lst[1] != None:
                                if row_date <= date_lst[1]:
                                    target_dict[row[header]] += 1
                            else:
                                if row_date <= date_lst[1] and row_date >= date_lst[0]:
                                    target_dict[row[header]] += 1