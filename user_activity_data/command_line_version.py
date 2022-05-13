import logging
import sys
import datetime
import create_application_csv
import create_user_csv


def main() -> None:
    """ Simple program to rank users, country and application based on the 
    activity data for the month of August 2021 from csv files.

    Takes either zero or two command line arguments. 
    
    - Args must be integers between 1 and 31 inclusive, and represent a 
    range of days in August 2021. The program will not consider any user, 
    country, or application activity outside of the range
    August (smaller arg) 2021 to August (larger arg) 2021, inclusive.

    - If used without arguments, all files will be parsed without
    consideration for "date" cell data.

    - If used with two arguments, the smaller arg will be the lower bound on
    the range of days, and the larger arg will be the upper bound. Rows of 
    CSV files missing "date" data will not be parsed in this case.
    """
    # Create a list of command line args
    args = sys.argv[1:]
    
    
    if len(args) == 0:
        # If user inputs no command line args, leave input_dates as None
        pass
    elif len(args) == 2:
        # Sets input_dates of called files
        try:
            from_date = datetime.datetime(2021, 8, min(int(args[0]), int(args[1])))
            to_date = datetime.datetime(2021, 8, max(int(args[0]), int(args[1])))
        except ValueError:
            logging.error("Command line arguments must be integers between"
            "1 and 31 inclusive.")
            exit(1)

        create_application_csv.input_dates[0] = from_date
        create_user_csv.input_dates[0] = from_date

        create_application_csv.input_dates[1] = to_date
        create_user_csv.input_dates[1] = to_date
    else:
        logging.error("Incorrect number of arguments.\nUsage: python3"
                    " user_main.py from_date to_date")
        exit(1)

    
    create_application_csv.main()
    # create_user_csv.main()
    


if __name__ == "__main__":
    main()