import re

with open('pyproject.toml', 'r') as f:
    __version__ = re.search(r'^version\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)
