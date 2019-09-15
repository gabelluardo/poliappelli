PE := PIPENV_VENV_IN_PROJECT
SP := __main__.py

all: compile clean
.PHONY: all

compile:
	$(PE)=1 pipenv install
	pipenv run pyinstaller --onefile $(SP) -n script
	mv dist/* .

clean:
	rm -rf __pycache__/ build/ dist/ *.spec *.log .venv/
