import pandas as pd
import os

path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

def main() -> None:
    count = 0
    for i in range(1, 6):
        df = pd.read_csv(parent_path + "/" + "csv_files/activity_" + str(i) 
            + ".csv")
        for index, row in df.iterrows(): 
            if row["application"] == "Safari" and row["date"] == "2021-08-24":
                count += 1

    print(count)


if __name__ == "__main__":
    main()