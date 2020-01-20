SP := poliappelli/__main__.py
URL := https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz

all: install clean
.PHONY: all

install:
	mkdir driver
	curl -L $(URL) | tar zxv -C driver
	poetry install --no-root
	poetry run pyinstaller $(SP) -n poliappelli --onefile --add-binary "./driver/geckodriver:./driver" --add-data "pyproject.toml:."

clean:
	rm -rf */__pycache__/ build/ *.spec *.log *.egg-info driver
	rm -rf .venv/ 
