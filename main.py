
import os
import subprocess
import datetime as dt
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
    echo "{r_message}" >> README.md
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



while True:
    current_date = dt.datetime.now()
    readme_message = "Last commit - {0}\n".format(current_date)
    run_git_script(uuid.uuid1(), readme_message)
 
    hour_in_seconds = 60 * 60
    sleep_time = random.randint(hour_in_seconds * 0.8, hour_in_seconds * 1.2)

    DIR=os.environ['GITHUB_REPOSITORY']
    if not os.path.exists('{dir}'.format(dir = DIR)):
        sleep_time = 5

    time.sleep(sleep_time)