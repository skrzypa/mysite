from django.test import TestCase


# Create your tests here.
import pytest

from .beercalc import BeerCalc



bc = BeerCalc()



def test_baling_to_brix():
    assert bc.baling_to_brix("14") == 14.56


def test_baling_to_brix_None():
    assert bc.baling_to_brix("14a") is None
    

def test_brix_to_baling():
    assert bc.brix_to_baling("21") == 20.19
    

def test_brix_to_baling_None():
    assert bc.brix_to_baling("2a1") is None


def test_baling_to_percent():
    assert bc.baling_to_percent('15', '3') == 6.19


def test_baling_to_percent_None():
    assert bc.baling_to_percent('15', '3a') is None


def test_brix_to_percent():
    assert bc.brix_to_percent('18', '4') == 6.95


def test_brix_to_percent_None():
    assert bc.brix_to_percent('18a', '4') is None


def test_how_much_sugar():
    assert bc.how_much_sugar('2.5', '20', '22') == 136.34


def test_how_much_sugar_None():
    assert bc.how_much_sugar('2.5', '20a', '22') is None


def test_sugar_solution():
    assert bc.sugar_solution('18', '136.34') == 757.44


def test_sugar_solution_None():
    assert bc.sugar_solution('18', '136.34a') is None