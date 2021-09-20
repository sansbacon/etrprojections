# etrprojections/etrprojections/__init__.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

from .etr import Scraper, Parser, ETRProjections

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())