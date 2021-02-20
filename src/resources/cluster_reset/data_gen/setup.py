""" Project installation configuration """

from setuptools import setup, find_packages

setup(
    name="data_gen",
    version="0.1.4",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'generate-data=data_gen.cli:handle'
        ]
    },

)
