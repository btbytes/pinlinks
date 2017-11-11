all:
	python pinlinks.py -y `date +%Y` -m `date +%m` > ~/www.btbytes.com/links/`date +%Y-%m`.md
