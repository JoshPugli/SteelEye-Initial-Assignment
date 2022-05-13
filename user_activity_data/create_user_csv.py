import ipaddress
import numpy as np
from pseudo_header import parent_path, init_df_dict
import pandas as pd
from ipwhois import IPWhois


country_data_unsorted = {"country_name": [], "country_code": [], 
    "total_hits": []}
user_data_unsorted = {"user_id": [], "first_name": [], "last_name": [], 
    "email": [], "total_hits": []}

country_data = {"country_name": [], "country_code": [], "total_hits": []}
user_data = {"user_id": [], "first_name": [], "last_name": [], "email": [], 
            "total_hits": []}

# Initializes input dates. This is mutated by user input through main.py
input_dates = [None, None]


def main():
    """Parses through the activity & user dataset files and create following 
    csv files: 

    - top 10 most active users in descending order with following 
    columns -> user_id, first_name, last_name, email, total_hits
    - top 3 applications used to browse websites. It should have the 
    following columns -> application_name, total_hits

    Since there are no source_ip values from the activity files that match 
    any ip_address values from user_dataset, this file looks up whois data 
    for each source_ip from activity files to find ip networks (ranges of ip 
    addresses) that may contain user ip addresses. In the case where there is 
    multiple user ips on the same network, divide the number of hits for each 
    user by the number of users on the network to get the statistical average
    of hits.

    Since whois lookup is very expensive, this function writes all data to 
    a file to avoid looking up data for any address more than once. Assuming a 
    fixed number of source ips, this reduces the amortized cost of whois 
    lookup to be order number of source ips.
    """

    ip_dict = {}
    
    init_df_dict("source_ip", ip_dict, input_dates)

    old_data = ""
    cidr_dict = {}

    # If IP_ranges.txt is initialized, populate cidr_dict with the cidr range
    # data contained in "IP_ranges.txt"
    try:
        f = open("IP_ranges.txt", "r")
        old_data = f.read()

        old_data_lst = old_data.split(" ")
        f.close()
        cidr_dict = {}

        for kv_pair in old_data_lst:
            kv_pair = kv_pair.split(":")
            if len(kv_pair) == 2:
                cidr_dict[kv_pair[0]] = [kv_pair[1]]
                prev_key = kv_pair[0]
            elif len(kv_pair) == 1:
                if kv_pair == [""]:
                    pass
                elif kv_pair[0][-1] == ",":
                    kv_pair[0] = kv_pair[0][:-1]
                    cidr_dict[prev_key].append(kv_pair[0])
                else:
                    cidr_dict[prev_key].append(kv_pair[0])

            else:
                pass
    except FileNotFoundError:
        pass
    
    
    cidr_str = old_data
    current_ips = {}

    for key in ip_dict:
        # Add key and its cidr range to the dict of current ips for this 
        # run of the program
        if key not in cidr_dict:
            # If there is an ip address that had not been previously analyzed,
            # get its whois data and add it to the string to be written to
            # IP_ranges.txt
            obj = IPWhois(key)
            results = obj.lookup_whois()

            cidr = results["nets"][0]["cidr"]
            cidr_str += key + ":" + cidr + " "
            try:
                current_ips[key].append(cidr)
            except KeyError:
                current_ips[key] = [cidr]
        else:
            current_ips[key] = (cidr_dict[key])

    # Write any new data to 'IP_ranges.txt' to store the data between runs
    # of the program
    with open("IP_ranges.txt", "w") as data: 
        data.write(str(cidr_str))

    df = pd.read_csv(parent_path + "/" + "csv_files/user_dataset.csv")

    address_matches = {}

    # Search ip addresses in user_dataset to see if any are within a network
    for key in current_ips:
        for value in current_ips[key]:
            for index, row in df.iterrows():
                hits = ip_dict[key]
                try:
                    an_address = ipaddress.ip_address(row["ip_address"])
                    a_network = ipaddress.ip_network(value)

                    address_in_network = an_address in a_network
                    # If the address is in a network, either add it to the 
                    # list of addresses in the network, or add a new key value  
                    # pair if there are currently no addresses in that network.
                    if address_in_network:
                        try:
                            address_matches[a_network].append([row["id"], 
                                row["first_name"], row["last_name"], 
                                row["email"], row["country"], 
                                row["country_code"], hits])
                        except KeyError:
                            address_matches[a_network] = [[row["id"], 
                                row["first_name"], row["last_name"], 
                                row["email"], row["country"], 
                                row["country_code"], hits]]
                except ValueError:
                    pass
    
    # Take data from each address in each network in address_matches, and
    # create an unsorted collection of data
    for address in address_matches:
        length = len(address_matches[address])
        for user in address_matches[address]:
            if pd.notna(user[0]):
                user_data_unsorted["user_id"].append(user[0])
                user_data_unsorted["first_name"].append(user[1])
                user_data_unsorted["last_name"].append(user[2])
                user_data_unsorted["email"].append(user[3])
                user_data_unsorted["total_hits"].append(user[6] / length)
            
            if pd.notna(user[4]):
                if user[4] not in country_data_unsorted["country_name"]:
                    country_data_unsorted["country_name"].append(user[4])
                    country_data_unsorted["country_code"].append(user[5])
                    country_data_unsorted["total_hits"].append(user[6] 
                        / length)
                else:
                    # If the country of the activity is already in the list,
                    # add the hits from this address to the countries total.
                    i = country_data_unsorted["country_name"].index(user[4])
                    country_data_unsorted["total_hits"][i] += (user[6] 
                        / length)

    # Sort the unsorted data for each data set in decreasing order of total 
    # hits, up to 3 and 10, respectively. If there aren't enough users or 
    # countries to fill the csv file, pad the rest of the rows with NaN
    # values.
    for i in range(0, 3):
        try:
            maximum = max(country_data_unsorted["total_hits"])
            max_index = country_data_unsorted["total_hits"].index(maximum)
        except Exception:
            pass

        for key in country_data_unsorted:
            try:
                country_data[key].append(country_data_unsorted[key][max_index])
                country_data_unsorted[key].pop(max_index)
            except Exception:
                country_data[key].append(np.nan)

    for i in range(0, 10):
        try:
            maximum = max(user_data_unsorted["total_hits"])
            max_index = user_data_unsorted["total_hits"].index(maximum)
        except Exception:
            pass

        for key in user_data_unsorted:
            try:
                user_data[key].append(user_data_unsorted[key][max_index])
                user_data_unsorted[key].pop(max_index)
            except Exception:
                user_data[key].append(np.nan)

    # Turn the sorted data into csv files.
    country_df = pd.DataFrame(country_data)  
    country_df.to_csv("top_3_countries.csv", index=False)

    user_df = pd.DataFrame(user_data)  
    user_df.to_csv("top_10_users.csv", index=False)




