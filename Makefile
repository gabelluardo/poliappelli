PE := PIPENV_VENV_IN_PROJECT
SP := poliappelli/__main__.py

all: install clean
.PHONY: all

install:
	$(PE)=1 pipenv install 
	pipenv run pyinstaller $(SP) -n poliappelli --onefile
#	 mv dist/* .

clean:
	rm -rf */__pycache__/ build/ *.spec *.log *.egg-info
#   rm -rf .venv/ dist/
