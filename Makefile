PE := PIPENV_VENV_IN_PROJECT
SP := __main__.py

all: install clean
.PHONY: all

install:
	$(PE)=1 pipenv install 
	pipenv run pyinstaller $(SP) -n script --onefile
	mv dist/* .

clean:
	rm -rf __pycache__/ build/ dist/ *.spec *.log .venv/
