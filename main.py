
import os
import subprocess
import datetime as dt
import git
import time


while True:
    current_date = dt.datetime.now()
    readme_message = "Last commit - {0}\n".format(current_date)

    bash_script = '''
    git config --global user.email {git_email}
    git config --global user.name {git_username}
    git clone {github_url}/{repository}.git
    cd {repository}
    git remote set-url origin https://{git_username}:{git_password}@github.com/{git_username}/{repository}.git
    git pull origin master
    touch README.md
    echo "{message}" >> README.md
    git add "README.md"
    git commit -a -m "Updated"
    git push origin master
    cd --
    rm -r -d -f {repository}
    '''.format(
        git_username = os.environ['GITHUB_USERNAME'],
        git_email = os.environ['GITHUB_EMAIL'],
        git_password = os.environ['GITHUB_PASSWORD'],
        github_url = "https://github.com/sanstorik",
        repository = "git_commits_incrementer",
        message = readme_message
    )

    subprocess.run(bash_script, shell = True, check = True, executable = '/bin/bash')

    time.sleep(10)