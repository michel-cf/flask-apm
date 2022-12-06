from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="Flask-Apm",
    install_requires=[
        'Flask>=0.8',
        'Blinker',
        'Flask-sqlalchemy>=3.0',
        'itsdangerous',
        'werkzeug',
    ],
)