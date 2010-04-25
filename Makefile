all:
	@echo Want to make update, server, or push?

server:
	../google_appengine/dev_appserver.py .

update:
	../google_appengine/appcfg.py update .

push:
	git push assembla master
