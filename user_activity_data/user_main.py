import pandas as pd
import datetime
import create_application_csv
import create_user_csv
import os
import platform


def clear():
   if platform.system() == 'Windows':
      os.system('cls')
   else:
      os.system('clear')


def main() -> None:
    # Extract from_date from user input
    clear()

    while 1:
        from_date_cmd_line = input("Enter lower bound on dates inluded in" 
            " search. If you do not wish to include a lower bound, leave"
            " blank and press ENTER.\nUsage: Year Month Day (YYYY MM DD)\n")
        
        clear()
        from_date_lst = from_date_cmd_line.split()
        
        if from_date_lst == []:
            break
        elif len(from_date_lst) == 3:
            from_date = datetime.datetime(int(from_date_lst[0]), 
                            int(from_date_lst[1]), int(from_date_lst[2]))
            
            create_application_csv.input_dates[0] = from_date
            create_user_csv.input_dates[0] = from_date
            break
        else:
            print("Incorrect Usage\n")
            
    

    # Extract to_date from user input
    while 1:
        to_date_cmd_line = input("Enter upper bound on dates inluded in" 
            " search. If you do not wish to include a upper bound, leave"
            " blank and press ENTER.\nUsage: Year Month Day (YYYY MM DD)\n")

        clear()
        to_date_lst = to_date_cmd_line.split()
        
        if to_date_lst == []:
            break
        elif len(to_date_lst) == 3:
            to_date = datetime.datetime(int(to_date_lst[0]), 
                            int(to_date_lst[1]), int(to_date_lst[2]))
            
            if to_date < from_date:
                print("Invalid input: Date must be greater than or equal to " 
                "lower bound.\n")
            else:
                create_application_csv.input_dates[1] = to_date
                create_user_csv.input_dates[1] = to_date
                break
        else:
            print("Incorrect Usage\n")
    
    create_application_csv.main()
    create_user_csv.main()
    


if __name__ == "__main__":
    main()