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

commit_data_map = {"commit_hash": "sha", "commit_message": "commit.message", "commit_url": "html_url",
 "author_name": "commit.author.name", "author_username": "author.login", "author_email": "commit.author.email", 
 "author_url": "author.html_url", "committer_name": "commit.committer.name", "committer_username": "committer.login", "committer_email": "commit.committer.email", 
 "committer_url": "committer.html_url", }

repo_data = {"repository_id": [], "repository_name": [], 
    "repository_url": [], "repository_fullname": [], "is_private": [], 
    "repository_description": [], "owner_username": [], "owner_url": [],
    "owner_type": [], "owner_site_admin": [], "is_fork": []}


commit_data = {"commit_hash": [], "commit_message": [], 
    "commit_url": [], "author_name": [], "author_username": [], 
    "author_email": [], "author_url": [], "committer_name": [],
    "committer_username": [], "committer_email": [], "committer_url": []}


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
    repo_data_df.to_csv("repo_details_.csv", 
                        index=False)
    

    for index, row in repo_data_df.iterrows():
        
        commit_url =  "https://api.github.com/repos/" + row["owner_username"] + "/" + row["repository_name"] + "/commits"
        print(commit_url)
        commits = requests.get(commit_url,headers=headers).json()

        for i in range(0, max_commit_count):
            for key in commit_data_map:
                code = commit_data_map[key].split(".")

                if len(code) == 1:
                    try:
                        commit_data[key].append(commits[i][code[0]])
                    except KeyError:
                        pass
                elif len(code) == 2:
                    try:
                        commit_data[key].append(commits[i][code[0]][code[1]])
                    except KeyError:
                        pass
                elif len(code) == 3:
                    try:
                        commit_data[key].append(commits[i][code[0]][code[1]][code[2]])
                    except KeyError:
                        pass
                else:
                    # Shouldn't get here
                    exit(1)
            commit_df = pd.DataFrame(commit_data)
            commit_df.to_csv("commits_" + row["repository_name"] + ".csv", index=False)      
            


if __name__ == "__main__":
    main()