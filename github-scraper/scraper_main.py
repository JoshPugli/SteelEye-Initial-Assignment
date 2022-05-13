import requests
import pandas as pd
import logging
import glob
import os

MAX_PARSE = 30


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


def create_repository_csvs(repository_count: int, 
        from_cmd_line: bool, headers=None) -> pd.DataFrame:
    """ Starting at "https://api.github.com/repositories?since=10000", 
    creates a csv file containing  repository_id, repository_name, 
    repository_url, repository_fullname, is_private, repository_description, 
    owner_username (github username), owner_url, owner_type, 
    owner_site_admin and is_fork for the next repository_count repositories.
    """
    try:
        # Create list of repositories starting at url
        url = "https://api.github.com/repositories?since=10000"
        if from_cmd_line:
            repos = requests.get(url, headers=headers).json()
        else:
            repos = requests.get(url).json()
    except Exception as e:
        logging.exception("Exception occurred")
        exit(1)
    
    # If the get request fails, repos will be set to the following.
    if repos == {'message': 'Bad credentials',
            'documentation_url': 'https://docs.github.com/rest'}:
        logging.error("Invalid credentials. Make sure that you are using "
        "a valid access token, and that you have not exceeded your limit for "
        "Github API calls.")
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
    return pd.DataFrame(repo_data)  


def create_commit_csvs(max_commit_count: int, df: pd.DataFrame, 
        from_cmd_line: bool, headers=None) -> None:
    """Takes in a pandas dataframe containing repository information, and 
    creates a new csv file for each repository in df.

    Starting from the earliest commit, each csv file contains commit info for 
    the first max_commit_count commits from its corresponding repository.

    Keys of csv files:
    - commit_hash, commit_message, commit_url, author_name, author_username, 
    author_email, author_url , committer_name, committer_username, 
    committer_email, committer_url
    """
    for index, row in df.iterrows():

        commit_data = {"commit_hash": [], "commit_message": [], 
            "commit_url": [], "author_name": [], "author_username": [], 
            "author_email": [], "author_url": [], "committer_name": [],
            "committer_username": [], "committer_email": [],
            "committer_url": []}
        
        commit_url =  ("https://api.github.com/repos/" + row["owner_username"] 
            + "/" + row["repository_name"] + "/commits")

        if from_cmd_line:
            commits = requests.get(commit_url, headers = headers).json()
        else:
            commits = requests.get(commit_url).json()

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
                            commit_data[key].append(commits[i][code[0]]
                                [code[1]])
                        except KeyError:
                            pass
                        except TypeError:
                            commit_data[key].append('None')
                    elif len(code) == 3:
                        try:
                            commit_data[key].append(commits[i][code[0]]
                                [code[1]][code[2]])
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


def run_program(repository_count: int, max_commit_count: int, 
    from_cmd_line=False, headers=None):
    """ Program that starts from 
    https://api.github.com/repositories?since=10000 and extracts the data 
    for all repositories into single csv file, and extracts commit details 
    from each repository into CSV files.

    If ran by command line, called programs use uer inputted GitHub personal 
    access tokens. Otherwise, program is run without.

    Params:
    - repository_count: number of repositories examined by the program
    - max_commit_count: maximum number of commits examined for each repository
    (if total number of commits is less than this parameter, only deals with 
    total number of commits for the repository)
    - from_cmd_line: should only be true when called from main(). Allows 
    functions to utilize user inputted personal access tokens when true
    - headers: should only be changed when from_cmd_line is True. 
    Contains info for personal access tokens, and is used in called functions.

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

    if (not isinstance(repository_count, int) or not 
        isinstance(max_commit_count, int)):
        logging.error("Incorrect parameter type: Parameters must be "
            "integers.")
        exit(1)

    if not ((1 <= repository_count <= MAX_PARSE) and 
            (1 <= max_commit_count <= MAX_PARSE)):
        logging.error("Parameters must be between 1 and " 
            + str(MAX_PARSE) + " inclusive.")
        exit(1)


    df = create_repository_csvs(repository_count, from_cmd_line, headers)
    create_commit_csvs(max_commit_count, df, from_cmd_line, headers) 
            

def main():
    logging.info("Running scraper_main.py...\n")
    key_in = input("Type two space seperated integers between 1 and " 
        + str(MAX_PARSE) + ", representing repository_count and "
        "max_commit_count.\n")
    
    args = key_in.split(" ")
    if len(args) != 2:
        logging.error("Incorrect number of parameters.")
        exit(1)
    
    try:
        repository_count = int(args[0])
        max_commit_count = int(args[1])
    except Exception:
        logging.error("Incorrect type for parameters: Parameters must "
            "be integers")
        exit(1)
    
    access_token = input("Input github access token.\n")
    headers = {'Authorization':"Token " + access_token}
    run_program(repository_count, max_commit_count, True, headers)
    


if __name__ == "__main__":
    main()