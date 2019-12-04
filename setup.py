import setuptools
import re

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('poliappelli/__init__.py', 'r') as f:
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
    entry_points={'console_scripts': ['poliappelli=poliappelli.__main__:main'], },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    install_requires=[
        'tqdm==4.40.0',
        'selenium==3.141.0',
        'beautifulsoup4==4.8.1',
        'beautifultable==0.8.0'
    ],
    extras_require={'dev': ['PyInstaller==3.5', 'pylint', 'autopep8']},
)
