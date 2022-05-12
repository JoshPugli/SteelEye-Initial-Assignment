import sys
import requests
import pandas as pd
import logging
import glob
import os

# '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' 
access_token = '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' 
headers = {'Authorization':"Token " + access_token}

repo_data_map = {"repository_id": "id", "repository_name": "name", 
    "repository_url": "html_url", "repository_fullname": "full_name",
    "is_private": "private", "repository_description": "description", 
    "owner_username": "login", "owner_url": "html_url",
    "owner_type": "type", "owner_site_admin": "site_admin", 
    "is_fork": "fork"}

commit_data_map = {"commit_hash": "sha", "commit_message": "commit.message", 
    "commit_url": "html_url", "author_name": "commit.author.name", 
    "author_username": "author.login", "author_email": "commit.author.email", 
    "author_url": "author.html_url", "committer_name": "commit.committer.name", 
    "committer_username": "committer.login", 
    "committer_email": "commit.committer.email", 
    "committer_url": "committer.html_url", }

repo_data = {"repository_id": [], "repository_name": [], 
    "repository_url": [], "repository_fullname": [], "is_private": [], 
    "repository_description": [], "owner_username": [], "owner_url": [],
    "owner_type": [], "owner_site_admin": [], "is_fork": []}


def main():
    """ Program that starts from 
    https://api.github.com/repositories?since=10000 and extracts the data 
    for all repositories into single csv file, and extracts commit details 
    from each repository into CSV files.

    - Takes two command line arguments, which must be integers between 1 and
    30:

    - repository_count: number of repositories examined by the program

    - max_commit_count: maximum number of commits examined for each repository
    (if total number of commits < Parameter 2, only deals with total number
    of commits for the repository)
    """
    # Remove all CSV files in directory, so that created CSV files are 
    # only the files created on a specific run of the program
    files = glob.glob("*.csv", recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            logging.exception("Exception occurred: %s", e)
            exit(1)


    args = sys.argv[1:]

    if len(args) != 2:
        logging.error("Incorrect number of arguments.\nUsage: python3"
                    " scraper_main repository_count max_commit_count")
        exit(1)

    try:
        repository_count = int(args[0])
        max_commit_count = int(args[1])
    except ValueError:
        logging.error("Command line arguments must be integers.")
        exit(1)

    if not (1 <= repository_count <= 30) or not (1 <= max_commit_count <= 30):
        logging.error("Command line arguments must be between 1 and 30" 
                    " inclusive.")
        exit(1)


    try:
        # Create list of repositories starting at url
        url = "https://api.github.com/repositories?since=10000"
        repos = requests.get(url, headers=headers).json()
    except Exception as e:
        logging.exception("Exception occurred")
        exit(1)
    

    for i in range (0, repository_count):
        for key in repo_data_map:
            try:
                # If key is non-nested
                repo_data[key].append(repos[i][repo_data_map[key]])
            except KeyError:
                # json files for repos also have a nested json file with key 
                # "owner", so keys inside must be dealt with seperately
                repo_data[key].append(repos[i]["owner"][repo_data_map[key]])
            except Exception as e:
                logging.exception("Exception occurred: %s", e)


    # Export data to CSV file
    repo_data_df = pd.DataFrame(repo_data)  
    repo_data_df.to_csv("repo_details_.csv", 
                        index=False)
    

    for index, row in repo_data_df.iterrows():

        commit_data = {"commit_hash": [], "commit_message": [], 
            "commit_url": [], "author_name": [], "author_username": [], 
            "author_email": [], "author_url": [], "committer_name": [],
            "committer_username": [], "committer_email": [],
            "committer_url": []}
        
        commit_url =  "https://api.github.com/repos/" + row["owner_username"] + "/" + row["repository_name"] + "/commits"
        commits = requests.get(commit_url, headers = headers).json()

        for i in range(0, max_commit_count):

            try: 
                for key in commit_data_map:

                    # Create a list containing key for each level of nesting
                    # for commit json data
                    code = commit_data_map[key].split(".")
                    
                    # Commit json files are at most triple nested, so we have
                    # 3 cases to deal with each level of nesting.
                    if len(code) == 1:
                        try:
                            commit_data[key].append(commits[i][code[0]])
                        except KeyError:
                            # Ignore cases where section of commits DNE
                            pass
                        except TypeError:
                            # This is only raised if commits[i][code...] 
                            # tries to access a key with a value of None.
                            commit_data[key].append('None')
                    elif len(code) == 2:
                        try:
                            commit_data[key].append(commits[i][code[0]][code[1]])
                        except KeyError:
                            pass
                        except TypeError:
                            commit_data[key].append('None')
                    elif len(code) == 3:
                        try:
                            commit_data[key].append(commits[i][code[0]][code[1]][code[2]])
                        except KeyError:
                            pass
                        except TypeError:
                            commit_data[key].append('None')
                    else:
                        # Shouldn't get here
                        exit(1)
            except IndexError:
                # If max_commit_count > len(commits), only include the number
                # of total commits to the repo.
                pass
            
            # Turn commit data for each repo into a CSV fiel
            commit_df = pd.DataFrame(commit_data)
            commit_df.to_csv("commits_" + row["repository_name"] + ".csv",
                            index=False)      
            


if __name__ == "__main__":
    main()