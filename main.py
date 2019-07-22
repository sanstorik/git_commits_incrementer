
import os
import subprocess
import datetime as dt
import git
import time


def run_git_script(commit_message, readme_message):
    bash_script = '''
    git config --global user.email {git_email}
    git config --global user.name {git_username}
    git clone {github_url}/{repository}.git
    cd {repository}
    git remote set-url origin https://{git_username}:{git_password}@github.com/{git_username}/{repository}.git
    git pull origin master
    touch README.md
    echo "{r_message}" >> README.md
    git add "README.md"
    git commit -a -m {c_message}
    git push origin master
    cd --
    rm -r -d -f {repository}
    '''.format(
        git_username = os.environ['GITHUB_USERNAME'],
        git_email = os.environ['GITHUB_EMAIL'],
        git_password = os.environ['GITHUB_PASSWORD'],
        github_url = os.environ['GITHUB_URL'],
        repository = os.environ['GITHUB_REPOSITORY']
        c_message = commit_message,
        r_message = readme_message
    )

    subprocess.run(bash_script, shell = True, check = True, executable = '/bin/bash')



while True:
    current_date = dt.datetime.now()
    readme_message = "Last commit - {0}\n".format(current_date)
    run_git_script("incremented", readme_message)
    time.sleep(10)