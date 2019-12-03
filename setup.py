import setuptools
import re

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('pyxbee/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setuptools.setup(
    name='poliappelli',
    version=version,
    author='Gabriele Belluardo',
    author_email='gabriele.belluardo@outlook.it',
    description='Script for PoliTo exams',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/gabelluardo/poliappelli',
    packages=['poliappelli'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    install_requires=['tqdm', 'selenium', 'beautifulsoup4', 'beautifultable'],
    extras_require={'dev': ['PyInstaller', 'pylint', 'autopep8']},
)
