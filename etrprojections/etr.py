# etrprojections/etrprojections/etr.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License


"""
etr.py    

Library to scrape ETR projections

NOTE: Subscription is required
This library does not access to anything 'extra' that user didn't buy
It automates projections download for an authorized user (via browser_cookie3)

"""

import logging

import browser_cookie3
import pandas as pd
import requests

from nflprojections import ProjectionSource


class Scraper:
    """Scrape ETR projections"""

    BASE_URL = 'https://establishtherun.com'

    def __init__(self):
        """Creates Scraper instance"""
        self._s = requests.session()
        self._s.cookies = browser_cookie3.load()
        self.urls = {
            'all_all': f'{self.BASE_URL}/fantasy-point-projections/',
            'dk_main': f'{self.BASE_URL}/draftkings-projections/',
            'fd_main': f'{self.BASE_URL}/fanduel-projections/'
        }

    def get(self, url, headers=None, params=None):
        """Gets HTML response"""
        r = self._s.get(url, headers=headers, params=params)
        return r.text

    def get_projections(self, site_name='all', slate_name='all'):
        """Gets projections"""
        key = f'{site_name}_{slate_name}'
        url = self.urls.get(key)
        if not url:
            raise ValueError(f'Invalid site or slate: {site_name}, {slate_name}')
        return self.get(url)


class Parser:
    """Parse ETR Projections table"""

    def projections(self, html):
        """Parses projections HTML"""
        tbl = pd.read_html(html)
        return tbl[1]


class ETRProjections(ProjectionSource):
    """Standardizes projections from establishtherun.com
       NOTE: this is post-processing after valid download
    """

    COLUMN_MAPPING = {
        'DK Position': 'pos',
        'DK Salary': 'salary',
        'DK Projection': 'proj',
        'DK Value': 'value',
        'DK Ownership': 'ownership',
        'DKSlateID': 'dk_slate_id',
        'Opponent': 'opp',
        'Team': 'team',
        'Player': 'plyr'
    }

    def __init__(self, **kwargs):
        """Creates object"""
        kwargs['column_mapping'] = self.COLUMN_MAPPING
        kwargs['projections_name'] = 'etr'
        super().__init__(**kwargs)

    def load_raw(self):
        s = Scraper()
        p = Parser()
        return p.projections(s.get_projections(self.site_name, self.slate_name))

    def process_raw(self, df):
        """Processes raw dataframe"""
        df.columns = self.remap_columns(df.columns)
        if df['ownership'].dtype == str:
            df['ownership'] = df['ownership'].str.replace('%', '').astype(int)
        if df['salary'].dtype == str:
            df['salary'] = pd.to_numeric(df['salary'].str.replace('$', ''), errors='coerce').fillna(0).astype(int)
        df = df.dropna(thresh=7)
        df.loc[:, 'dk_slate_id'] = df.loc[:, 'dk_slate_id'].astype(int)
        return df

    def standardize(self, df):
        """TODO: figure out player-name standardization"""
        return df.assign(team=lambda x: self.standardize_teams(x.team),
                         plyr=lambda x: self.standardize_players(x.plyr),
                         pos=lambda x: self.standardize_positions(x.pos))


if __name__ == '__main__':
    pass