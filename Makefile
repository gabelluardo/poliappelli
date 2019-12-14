SP := poliappelli/__main__.py

all: install clean
.PHONY: all

install:
	poetry install --no-root
	poetry run pyinstaller $(SP) -n poliappelli --onefile
#	 mv dist/* .

clean:
	rm -rf */__pycache__/ build/ *.spec *.log *.egg-info
#   rm -rf .venv/ dist/
