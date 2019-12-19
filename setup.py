from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pmcbib',
    version='0.0.2.dev1',
    description='Validate bibtex files against PubMed database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LelouchLamperougeVI/pmcbib',
    author='HaoRan Chang',
    author_email='haoran.chang@mail.mcgill.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='latex bibtex pubmed citation',

    packages=find_packages(),
    python_requires='==3.7.*',
    install_requires=[
        'metapub',
        'bibtexparser',
        'python-Levenshtein',
        ],
    package_data={
        'pmcbib': ['data/config.json'],
    },

    entry_points={
        'console_scripts': [
            'pmcbib=pmcbib.__main__:main',
        ],
    },
)
