# etrprojections/setup.py
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Eric Truett
# Licensed under the MIT License


from setuptools import setup, find_packages

PACKAGE_NAME = "etrprojections"


def run():
    setup(name=PACKAGE_NAME,
          version="0.3",
          description="python library for getting/parsing etr projections",
          author="Eric Truett",
          author_email="eric@erictruett.com",
          license="MIT",
          packages=find_packages(),
          package_data={'tests': ["data/*.json"]},
          zip_safe=False)


if __name__ == '__main__':
    run()
