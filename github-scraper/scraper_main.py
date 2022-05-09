import sys
import requests
import pandas as pd


access_token = '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' 
headers = {'Authorization':"Token " + access_token}

repo_data_map = {"repository_id": "id", "repository_name": "name", 
    "repository_url": "html_url", "repository_fullname": "full_name",
    "is_private": "private", "repository_description": "description", 
    "owner_username": "login", "owner_url": "html_url",
    "owner_type": "type", "owner_site_admin": "site_admin", 
    "is_fork": "fork"}

repo_data = {"repository_id": [], "repository_name": [], 
    "repository_url": [], "repository_fullname": [], "is_private": [], 
    "repository_description": [], "owner_username": [], "owner_url": [],
    "owner_type": [], "owner_site_admin": [], "is_fork": []}


def main():
    args = sys.argv[1:]

    if len(args) != 2:
        print("Replace with logging later")
        exit(1)
    
    repository_count = int(args[0])
    max_commit_count = int(args[1])


    try:
    # to find all the repos' names from each page
        url = "https://api.github.com/repositories?since=10000"
        repos = requests.get(url,headers=headers).json()
    except:
        pass
    

    for i in range (0, repository_count):
        for key in repo_data_map:
            try:
                repo_data[key].append(repos[i][repo_data_map[key]])
            except:
                repo_data[key].append(repos[i]["owner"][repo_data_map[key]])
    
    repo_data_df = pd.DataFrame(repo_data)  
    repo_data_df.to_csv("repo_details.csv", index=False)

    
        


if __name__ == "__main__":
    main()