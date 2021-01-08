import csv
import json
import requests

def get_bugs_for_repo(github_org = 'pennylaneai'):
    
    url_for_repos = f'https://api.github.com/orgs/{github_org}/repos'
    repos = requests.get(url_for_repos)
    repos = repos.json()

    bug_db = []

    for repo in repos:
        repo_name = repo['name']
        issues_and_prs = requests.get(f'https://api.github.com/repos/pennylaneai/{repo_name}/issues')

        issues_and_prs = issues_and_prs.json()
        issues = [issue for issue in issues_and_prs if "pull_request" not in issue]

        bugs = [issue for issue in issues for label in issue['labels'] if 'bug' in label['name']]
        bug_db.append((repo_name, bugs))
    
    return bug_db

headers = ["#", "Date", "Date replied", "Channel Type", "Type", "Component", "Brief description"]

def create_csv(bug_db):

    # 1. Create the data fit for the csv files
    data = []

    for repo_name, bugs in bug_db:
        for bug in bugs:
            base_url = f'https://github.com/{github_org}/{repo_name}/issues/'

            bug_number_in_list = ""
            date = bug['created_at'].split('T')[0].replace('-','/')
            date_replied = ""
            channel_type = "GitHub"
            entry_type = "Bug"
            component = repo_name
            name = bug['title']

            num = bug['url'].split('/')[-1]
            url = base_url + num

            brief_desc = f'=HYPERLINK("{url}", "{name}")'

            desc = [bug_number_in_list, date, date_replied, channel_type, entry_type, component, brief_desc]

            data.append(desc)

    # 2. Write csv file
    with open('bugs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def get_markdown(bug_db):

    # 1. Create the markdown string
    data = []

    for repo_name, bugs in bug_db:
        for bug in bugs:
            base_url = f'https://github.com/{github_org}/{repo_name}/issues/'

            bug_number_in_list = ""
            date = bug['created_at'].split('T')[0].replace('-','/')
            date_replied = ""
            channel_type = "GitHub"
            entry_type = "Bug"
            component = repo_name
            name = bug['title']

            num = bug['url'].split('/')[-1]
            url = base_url + num

            brief_desc = f'=HYPERLINK("{url}", "{name}")'

            desc = [bug_number_in_list, date, date_replied, channel_type, entry_type, component, brief_desc]

            data.append(desc)


def need_new_readme(markdown):

def update_readme():
    pass
    # 1. check if need update
    # 2. update

if __name__ == "__main__":

    bug_db = get_bugs_for_repo()
    create_csv(bug_db)
    markdown = get_markdown(bug_db)

    if need_new_readme(markdown):
        update_readme(bug_db)
