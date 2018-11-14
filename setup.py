from setuptools import setup, find_packages


setup(name='scraper',
      version='1.0',
      packages=find_packages(),
      install_requires=[
        'beautifulsoup4==4.6.3',
        'selenium==3.14.1',
        'certifi==2018.10.15',
    ],
)
