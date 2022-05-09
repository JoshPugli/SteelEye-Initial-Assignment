import pandas as pd
import datetime
import create_application_csv
import create_user_csv

def main() -> None:

    # Extract from_date from user input
    from_date_cmd_line = input("Enter from date. \nUsage: type Year," 
                        " Month, Day. Leave blank to ignore.\n")
    
    from_date_lst = from_date_cmd_line.split()
    
    if from_date_lst == []:
        pass
    elif len(from_date_lst) == 3:
        from_date = datetime.datetime(int(from_date_lst[0]), 
                        int(from_date_lst[1]), int(from_date_lst[2]))
        
        create_application_csv.input_dates[0] = from_date
        create_user_csv.input_dates[0] = from_date
    else:
        print("incorrect usage")
        exit(1)
    

    # Extract to_date from user input
    to_date_cmd_line = input("Enter to date. \nUsage: type Year, Month, Day." 
        " Leave blank to ignore.\n")

    to_date_lst = to_date_cmd_line.split()
    
    if to_date_lst == []:
        pass
    elif len(to_date_lst) == 3:
        to_date = datetime.datetime(int(to_date_lst[0]), 
                        int(to_date_lst[1]), int(to_date_lst[2]))
        
        create_application_csv.input_dates[1] = to_date
        create_user_csv.input_dates[1] = to_date
    else:
        print("incorrect usage")
        exit(1)
    
    create_application_csv.main()
    create_user_csv.main()
    


if __name__ == "__main__":
    main()