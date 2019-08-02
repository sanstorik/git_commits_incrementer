
import os
import subprocess
from datetime import datetime, timedelta
import time
import random
import uuid

commits_by_date = {}
repository_name = "hidden_commit_factory"
git_username = "sanstorik"

def run_git_script(commit_message, readme_message):
    bash_script = '''
    DIR={repository}
    if [ ! -d "$DIR" ]; then
        git clone git@github.com:{git_username}/{repository}.git
    fi

    if [ -d "$DIR" ]; then
        cd {repository}
        git checkout master
        git pull origin master
        touch README.md
        echo "{r_message}" > README.md
        git add "README.md"
        git commit -a -m {c_message}
        git push origin master
        cd --
    fi
    '''.format(
        git_username = git_username,
        repository =repository_name,
        c_message = commit_message,
        r_message = readme_message
    )

    subprocess.run(bash_script, shell = True, check = True, executable = '/bin/bash')


def daily_amount_of_commits(date):
    is_working_day = current_date.weekday() < 5
    previous_day_date = (date - timedelta(1))
    previous_day_commits_count = commits_by_date.get(date_to_str(previous_day_date)) or 0
    needed_commits = previous_day_commits_count

    while needed_commits == previous_day_commits_count:
        commits_range = (12, 20) if is_working_day else (7, 13)
        needed_commits = random.randint(commits_range[0], commits_range[1])

    return needed_commits


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


while True:
    commit_uuid_message = uuid.uuid1()
    current_date = datetime.now()
    readme_message = "{uuid} - {date}".format(uuid = commit_uuid_message, date = current_date)
    run_git_script(uuid.uuid1(), readme_message)
 
    today_date = datetime.today()
    sleep_time = 0
    commits_amount = 0

    if date_to_str(today_date) in commits_by_date:
        commits_amount = commits_by_date[date_to_str(today_date)]
    else:
        commits_amount = daily_amount_of_commits(today_date)
        commits_by_date[date_to_str(today_date)] = commits_amount

    if not os.path.exists(repository_name):
        sleep_time = 5
    else:
        sleep_time = float(24 * 60 * 60) / float(commits_amount)

    time.sleep(sleep_time)