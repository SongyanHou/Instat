# Instat
Instat is a domain-specific programming language focusing on calling Instgram API in a super easy way.

# How to run it
python runInstat.py -i \<inputfile\>

Please check the Test files here 
https://github.com/oceanhuang/CoZy/tree/master/test/testFiles
to see the input format.


# Git Etiquette
+ Never modify *master* directly
+ Create a new branch for each feature: *git checkout -b 'MyBranch'*
+ Work on branches only, push to github repo: *git push*
+ Create a **pull request**: go to [git repo](https://github.com/SongyanHou/Instat), select your branch on top left corner, and create a pull request on top right corner.
+ Accept the pull request if you are confident; otherwise ask for code review.
+ **rebase** unmerged branch when it falls behind *master*
	- update your master branch: *git checkout master && git pull*
	- check out the branch you want to rebase: *git checkout MyBranch*
	- rebase you branch so that it absorbs new code from master:
	*git rebase master*
	- you may need to resolve merge conflicts before completing the rebase: *git --mergetool*
+ When in doubt: use google
