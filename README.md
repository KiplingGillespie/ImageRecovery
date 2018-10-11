# ImageRecovery
Project for CS 499 Senior Design at the University of Kentucky.

change to the directory you want to store the project in.
call:

git clone https://github.com/KiplingGillespie/ImageRecovery.git

to download repository files. There are best practices while developing and I will describe the work flow.

git pull 
to get any updates that have been pushed to the master repository. 

make your changes and/or create aditional files. Any new or changed files will need to be added by

git add filename

If you have files that you don't want to include such as elclips project files, don't add them.

git status

gives a list of files that are new and have been changed. Any changed files must be added before git will allow you to commit.

git commit -m "Message describing changes in commit."

commits act as check points you can go back to in case errors accidentally get pushed.

If you make more changes before pushing and need to commit again, you can call

git commit --amend 

will roll the changes into the previous commit and allow you to make changes to the commit comments. When your changes have been commited and are deemed bug free you may push your changes with

git push origin master


Atlassian has great git tutorials. Checkout the section on dealing with merge issues. Especially checkout "git rebase"
https://www.atlassian.com/git/tutorials/comparing-workflows

Let me know if you have any questions
- Kipling Gillespie
