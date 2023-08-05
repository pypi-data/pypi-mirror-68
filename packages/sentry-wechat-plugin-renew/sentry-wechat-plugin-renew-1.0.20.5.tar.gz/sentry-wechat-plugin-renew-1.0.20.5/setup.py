#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# See http://stackoverflow.com/questions/9352656/python-assertionerror-when-running-nose-tests-with-coverage
# for why we need to do this.
from multiprocessing import util
import sentry_wechat


tests_require = [
]

install_requires = [
    'sentry>=9.1.0',
    'requests',
    'pytz',
    'django',
]


setup(
    name='sentry-wechat-plugin-renew',
    version=sentry_wechat.VERSION,
    keywords='sentry wechat ',
    author='cxt',
    author_email='cxt1122jk@gmail.com',
    url='https://github.com/susujs/sentry-wechat-plugin.git',
    description='A Sentry extension which integrates with Wechat robot.',
    long_description='A Sentry extension which integrates with Wechat robot.',
    long_description_content_type='text/markdown',
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='nose.collector',
    entry_points={
        'sentry.plugins': [
            'wechat = sentry_wechat.plugin:WechatPlugin'
        ],
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)