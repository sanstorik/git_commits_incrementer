
import os
import subprocess
from datetime import datetime
import time
import random
import uuid


def run_git_script(commit_message, readme_message):
    bash_script = '''
    git config --global user.email {git_email}
    git config --global user.name {git_username}

    DIR={repository}
    if [ ! -d "$DIR" ]; then
        git clone {github_url}/{repository}.git
    fi

    cd {repository}
    git remote set-url origin https://{git_username}:{git_password}@github.com/{git_username}/{repository}.git
    git pull origin master
    touch README.md
    echo "{r_message}" > README.md
    git add "README.md"
    git commit -a -m {c_message}
    git push origin master
    cd --
    '''.format(
        git_username = os.environ['GITHUB_USERNAME'],
        git_email = os.environ['GITHUB_EMAIL'],
        git_password = os.environ['GITHUB_PASSWORD'],
        github_url = os.environ['GITHUB_URL'],
        repository = os.environ['GITHUB_REPOSITORY'],
        c_message = commit_message,
        r_message = readme_message
    )

    subprocess.run(bash_script, shell = True, check = True, executable = '/bin/bash')


def script_sleep_interval(date):
    hour_in_seconds = 60 * 60
    sleep_time = random.randint(hour_in_seconds * 0.8, hour_in_seconds * 1.3)

    is_working_day = current_date.weekday < 5
    is_working_hour = current_date.hour >= 9 and current_date.hour <= 18

    if not (is_working_day and is_working_hour):
        sleep_time *= 2.2

    return sleep_time



while True:
    commit_uuid_message = uuid.uuid1()
    current_date = datetime.now()
    readme_message = "{uuid} - {date}".format(uuid = commit_uuid_message, date = current_date)
    run_git_script(uuid.uuid1(), readme_message)
 

    sleep_time = script_sleep_interval(current_date)
    DIR = os.environ['GITHUB_REPOSITORY']
    if not os.path.exists('{dir}'.format(dir = DIR)):
        sleep_time = 5

    time.sleep(sleep_time)