import glob

from poliappelli import resource_path

GECKODRIVERS = {'Darwin': None, 'Windows': None, 'Linux': None}


def drivers():
    path = resource_path('driver')
    drivers = glob.glob(f'{path}/geckodriver*')

    for file in drivers:
        if 'macos' in file.split('-'):
            GECKODRIVERS.update({'Darwin': file})
        elif 'win64' in file.split('-'):
            GECKODRIVERS.update({'Windows': file})
        else:
            GECKODRIVERS.update({'Linux': file})
