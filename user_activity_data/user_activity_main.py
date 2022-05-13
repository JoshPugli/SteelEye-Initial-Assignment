import logging
import datetime
import sys
import create_application_csv
import create_user_csv

# python3 -c 'from user_activity_main import run_program; run_program()'

def run_program(from_date=None, to_date=None) -> None:
    """Simple program to rank users, country and application based on the 
    activity data for the month of August 2021 from csv files.
    
    - Parameters must be integers between 1 and 31 inclusive, and represent a 
    range of days in August 2021. The program will not consider any user, 
    country, or application activity outside of the range
    August (smaller arg) 2021 to August (larger arg) 2021, inclusive.

    - If used without arguments, all files will be parsed without
    consideration for "date" cell data.

    - If used with one or two parameters, from_date will be the lower bound on
    the range of days, and the to_date will be the upper bound. Rows of 
    CSV files missing "date" data will not be considered in this case.
    """

    if from_date != None:
        try:
            from_date = datetime.datetime(2021, 8, from_date)
        except TypeError:
            logging.error("Incorrect type for parameters: Parameters must "
                "be integers")
            exit(1)
    
    if to_date != None:
        try:
            to_date = datetime.datetime(2021, 8, to_date)
        except TypeError:
            logging.error("Incorrect type for parameters: Parameters must "
                "be integers")
            exit(1)
    

    create_application_csv.input_dates[0] = from_date
    create_user_csv.input_dates[0] = from_date

    create_application_csv.input_dates[1] = to_date
    create_user_csv.input_dates[1] = to_date


    
    create_application_csv.main()
    create_user_csv.main()
    


def main():
    logging.info("Running user_activity_main.py...\n")
    user_in = input("Type two space seperated integers between 1 and 31, "
        "representing from_date and to_date respectively. Press enter without "
        "typing to leave unbounded.\n")
    
    # Create list from command line args
    args = user_in.split(" ")
    
    flag = False
    if args == [''] or len(args) == 0:
        # If user inputs no command line args, run program with no input
        flag = True
    elif len(args) == 2:
        # Sets input_dates of called files
        try:
            from_date = int(args[0])
            to_date = int(args[1])
        except ValueError:
            logging.error("Command line arguments must be integers between"
            "1 and 31 inclusive.")
            exit(1)
    
    if flag:
        run_program()
    else:
        run_program(from_date, to_date)

    


if __name__ == "__main__":
    main()