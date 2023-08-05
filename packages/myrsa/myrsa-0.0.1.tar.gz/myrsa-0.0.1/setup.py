#coding=utf8

from setuptools import setup

from myrsa import VERSION


try:
    long_description = open('README.md', encoding='utf8').read()
except Exception as e:
    print(e)
    long_description = ''

setup(
    name='myrsa',
    version=VERSION,
    description='Simple use of RSA for asymmetric encryption and signature | 简单使用 rsa 进行非对称加密和签名',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
    install_requires=['rsa'],
    license='MIT License',
    py_modules=['myrsa'],
    platforms=["all"],
    url='https://github.com/taojy123/myrsa',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
