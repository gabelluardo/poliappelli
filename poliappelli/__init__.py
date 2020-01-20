import re
import sys
from os import path


def resource_path(relative_path):
    try:
        # pylint: disable=no-member
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.dirname(path.dirname(__file__))
    return path.join(base_path, relative_path)


with open(resource_path('pyproject.toml'), 'r') as f:
    __version__ = re.search(r'^version\s*=\s*[\'"]([^\'"]*)[\'"]',
                            f.read(), re.MULTILINE).group(1)
