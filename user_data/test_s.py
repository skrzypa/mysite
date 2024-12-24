from django.test import TestCase
from .password_checker import PasswordChecker
import pytest

# Create your tests here.
pass1 = PasswordChecker('412421421', '412421421')
def test_compare_1():
    assert pass1.compare_passwords() is True

def test_numerical_1():
    assert pass1.not_only_numerical() is False

def test_too_short_1():
    assert pass1.too_short() is False



pass2 = PasswordChecker('412421421', '4124214211')
def test_compare_2():
    assert pass2.compare_passwords() is False

def test_numerical_2():
    assert pass2.not_only_numerical() is False

def test_too_short_2():
    assert pass2.too_short() is False



pass3 = PasswordChecker('412421421gtdfsyhgfre', '412421421gtdfsyhgfre')
def test_compare_3():
    assert pass3.compare_passwords() is True

def test_numerical_3():
    assert pass3.not_only_numerical() is True

def test_too_short_3():
    assert pass3.too_short() is False



pass4 = PasswordChecker('hgfre', 'hgfre')
def compare_4():
    assert pass4.compare_passwords() is True

def numerical_4():
    assert pass4.not_only_numerical() is True

def too_short_4():
    assert pass4.too_short() is True