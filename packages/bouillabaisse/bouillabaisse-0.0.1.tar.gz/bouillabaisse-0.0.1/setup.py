# -*- coding: utf-8 -*-

# minimal setup.py to install in develop mode



from setuptools import setup, find_packages



setup(

    name="bouillabaisse",

    packages=find_packages(),



    # see https://semver.org/

    # and https://pypi.org/project/semver/

    version="0.0.1",



    author="Alex Grumberg",

    author_email="ag@gmail.com",

    description="recettes de bouillabaisse",

    #keywords=["Python", "package", "setup.py", "setuptools"],

    url="https://github.com/flotpython/bidule",

    license="Creative Commons BY-CC-ND 4.0",

)