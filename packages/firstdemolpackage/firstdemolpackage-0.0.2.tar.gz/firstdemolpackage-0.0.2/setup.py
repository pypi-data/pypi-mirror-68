#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='firstdemolpackage',
    version='0.0.2',
    description=(
        '打包测试'
    ),
    long_description=open('README.rst').read(),
    author='ken',
    author_email='xiaomishaona@126.com',
    maintainer='ken',
    maintainer_email='xiaomishaona@126.com',
    license='BSD License',
    # packages=find_packages(),
    packages=['firstdemolpackage'],
    platforms=["all"],
    url='http://www.baidu.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=['requests-html', 'six>=1.5.2']
)


# classifiers=[
#         'Development Status :: 4 - Beta',
#         'Operating System :: OS Independent',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: BSD License',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: Implementation',
#         'Programming Language :: Python :: 2',
#         'Programming Language :: Python :: 2.7',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7',
#         'Topic :: Software Development :: Libraries'
#     ],
