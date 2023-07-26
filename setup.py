# creat setip.py file

from setuptools import setup, find_packages

setup(
    name='pytorch-ssd',
    version='0.0.1',
    description='SSD: Single Shot MultiBox Detector, in PyTorch',
    author='Max deGroot, Ellis Brown',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
)
# Path: tests/test_initVar.py
# import unittest
# from LiveTune import initVar
#
# class TestInitVar(unittest.TestCase):
#
#     def test_initialization(self):

