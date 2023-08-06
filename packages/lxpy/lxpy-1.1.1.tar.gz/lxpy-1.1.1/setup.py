#-*- coding:utf-8 -*-
# @Author  : lx

from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'lxpy',
    version = '1.1.1',
    py_modules = ['lxpy'],
    author = 'ying5338619',
    author_email = '125066648@qq.com',
    url='https://github.com/lixi5338619/lxpy.git',
    #install_requires=["wheel"],
    description = 'Web crawler and data processing toolkit !',
    keywords = ['lx', 'crawl'],
    python_requires='>=3.4.0',  # python环境
    packages=find_packages()
)
