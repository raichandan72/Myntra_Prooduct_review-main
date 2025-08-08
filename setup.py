from setuptools import setup, find_packages
setup (
    name='scrapper',
    version='0.1',
    author='Chandan Roy',
    author_email='atchandanworkspace@gmail.com',
    description='scrapper',
    packages=find_packages(),
        install_requires=[
        "streamlit",
        "pandas",
        "pymongo",
        "plotly",
        "database-connect",
        "requests",
        "beautifulsoup4"
    ]
)