all:
	@echo Things to make:
	@echo server           - loads up the dev webserver
	@echo update-force     - uploads the contents of the current directory to the appengine
	@echo gitpull          - pull --rebase both master+live branches on current git repo
	@echo pushlive         - pushes the live branch to assembla _and_ makes it live

server:
	../google_appengine/dev_appserver.py .

update-force:
	../google_appengine/appcfg.py update .

gitpull:
	@echo Fetching..
	git fetch --verbose assembla
	@echo Stashing..
	git stash
	@echo Updating master..
	git checkout master
	git pull --rebase assembla master
	@echo Updating live..
	git checkout live
	git pull --rebase assembla live
	@echo Back to master, stash:
	git checkout master
	git stash list

gitpush:
	@echo Stashing..
	git stash
	@echo Git pushing master..
	git checkout master
	git push assembla master
	@echo Git pushing live..
	git checkout live
	git push assembla live
	@echo Back to master, stash:
	git checkout master
	git stash list

pushlive:
	@echo Stashing..
	git stash
	@echo Updating Git live..
	git checkout live
	git fetch --verbose assembla
	git pull --rebase assembla live
	git push assembla live
	@echo Pushing app live..
	../google_appengine/appcfg.py update .

