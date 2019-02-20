PE := PIPENV_VENV_IN_PROJECT
SP := script.py
VE := .venv/

target:
	export $(PE)=1;\
	pipenv install
	pipenv run pyinstaller --onefile $(SP)
	mv dist/* .

clean:
	rm -rf __pychache__/ build/ dist/ *.spec *.log $(VE)
