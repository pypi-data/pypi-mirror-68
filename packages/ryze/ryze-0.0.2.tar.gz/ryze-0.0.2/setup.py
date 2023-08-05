from setuptools import setup

from ryze import __version__

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='ryze',
    version=__version__,
    author='André Sousa',
    author_email='andrematosdesousa@gmail.com',
    description='League of Legends game updates wrapper and scrapper',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['ryze'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
    project_urls={
        'Source': 'https://github.com/sousa-andre/ryze'
    }
)
