import sys
import pandas as pd
import datetime
import create_application_csv
import create_user_csv


def main() -> None:
    # Extract from_date from user input

    args = sys.argv[1:]
    

    if len(args) == 0:
        pass
    elif len(args) == 2:
        from_date = datetime.datetime(2021, 8, min(int(args[0]), int(args[1])))
        to_date = datetime.datetime(2021, 8, max(int(args[0]), int(args[1])))

        create_application_csv.input_dates[0] = from_date
        create_user_csv.input_dates[0] = from_date

        create_application_csv.input_dates[1] = to_date
        create_user_csv.input_dates[1] = to_date
    else:
        # Incorrect Usage
        exit(1)

    
    create_application_csv.main()
    create_user_csv.main()
    


if __name__ == "__main__":
    main()