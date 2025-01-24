from django.test import TestCase

# Create your tests here.
import pytest

from .beer_calc import BeerCalc



bc = BeerCalc()

def test_baling_to_brix_str():
    assert bc.baling_to_brix("1") == 1.04

def test_baling_to_brix_int():
    assert bc.baling_to_brix(1) == 1.04

def test_baling_to_brix_float():
    assert bc.baling_to_brix(1.0) == 1.04

def test_baling_to_brix_None():
    assert bc.baling_to_brix('a') is None



def test_brix_to_baling_str():
    assert bc.brix_to_baling('1') == 0.96

def test_brix_to_baling_int():
    assert bc.brix_to_baling(1) == 0.96

def test_brix_to_baling_float():
    assert bc.brix_to_baling(1.0) == 0.96

def test_brix_to_baling_None():
    assert bc.baling_to_brix('a') is None



def test_brix_to_alc_str():
    assert bc.brix_to_percent('11', '1') == 4.96

def test_brix_to_alc_int():
    assert bc.brix_to_percent(11, 1) == 4.96

def test_brix_to_alc_float():
    assert bc.brix_to_percent(11.0, 1.0) == 4.96

def test_brix_to_alc_None_1():
    assert bc.brix_to_percent(11.0, 'a') is None

def test_brix_to_alc_None_2():
    assert bc.brix_to_percent('a', 1) is None



def test_blg_to_alc_str():
    assert bc.baling_to_percent('11', '1') == 5.16

def test_blg_to_alc_int():
    assert bc.baling_to_percent(11, 1) == 5.16

def test_blg_to_alc_float():
    assert bc.baling_to_percent(11.0, 1.0) == 5.16

def test_blg_to_alc_None_1():
    assert bc.baling_to_percent(11.0, 'a') is None

def test_blg_to_alc_None_2():
    assert bc.baling_to_percent('a', 1.0) is None