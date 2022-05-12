import logging
import datetime
import create_application_csv
import create_user_csv

# python3 -c 'from user_activity_main import main; main()'

def run_program(from_date=None, to_date=None) -> None:
    """ Simple program to rank users, country and application based on the 
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
    # create_user_csv.main()
    


def main():
    run_program()


if __name__ == "__main__":
    main()