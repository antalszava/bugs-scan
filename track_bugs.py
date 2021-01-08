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

def track_bugs():

    # 1. Get the bugs for an organization
    github_org = 'pennylaneai'
    bug_db = get_bugs_for_repo(github_org)

    # 2. Create the data fit for the csv files
    data = []
    csv_headers = ["#", "Date", "Date replied", "Channel Type", "Type", "Component", "Brief description"]

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

    # 3. Write csv file
    with open('bugs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    track_bugs()
