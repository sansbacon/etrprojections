import pandas as pd
import pytest
import requests_mock

from etrprojections import Scraper, Parser, ETRProjections


def test_etr_scraper():
    """Tests etr scraper"""
    s = Scraper()


def test_etr_scraper_get():
    """Tests etr scraper"""
    s = Scraper()
    url = 'https://www.google.com'
    assert 'Google' in s.get(url)
    

def test_etr_scraper_get_projections():
    """Tests etr scraper"""
    s = Scraper()
    assert 'LAST UPDATED' in s.get_projections()


def test_etr_parser_projections():
    """Tests etr scraper"""
    s = Scraper()
    p = Parser()
    proj = p.projections(s.get_projections())
    assert isinstance(proj, pd.DataFrame)
    assert 'Position' in proj.columns


def test_etr_projection_source(test_directory):
    """Tests ETR projection source"""
    with pytest.raises(TypeError):
        e = ETRProjections()
    e = ETRProjections(rawdir=test_directory, procdir=test_directory)
    assert isinstance(e, ETRProjections)


@requests_mock.Mocker(kw='mock')
def test_etr_load_raw(test_directory, **kwargs):
    kwargs['mock'].get(requests_mock.ANY, text=(test_directory / 'etr.html').read_text())
    e = ETRProjections(rawdir=test_directory, procdir=test_directory)
    assert isinstance(e.load_raw(), pd.DataFrame)    

