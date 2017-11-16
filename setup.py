from setuptools import setup, find_packages

setup(
    name='ff-metadata',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click>=6.6',
        'Flask>=0.11.1',
        'itsdangerous>=0.24',
        'Jinja2>=2.8',
        'MarkupSafe>=0.23',
        'MySQL-python>=1.2.5',
        'Werkzeug>=0.11.11'
    ]
)
