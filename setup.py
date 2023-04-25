#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'google-api-core==2.11.0',
    'google-api-python-client==2.86.0',
    'google-auth==2.17.3',
    'google-auth-httplib2==0.1.0',
    'google-auth-oauthlib==1.0.0',
    'googleapis-common-protos==1.59.0',
    'requests==2.28.2'
    ]

test_requirements = ['pytest>=3', ]

setup(
    author="Kjartan Akil Jonsson",
    author_email='kjartan@modeller.dev',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Modeller BP wrapping email services",
    entry_points={
        'console_scripts': [
            'modelbp_wrap_email=modelbp_wrap_email.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='modelbp_wrap_email',
    name='modelbp_wrap_email',
    packages=find_packages(include=['modelbp_wrap_email', 'modelbp_wrap_email.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/modellers/modelbp_wrap_email',
    version='0.1.0',
    zip_safe=False,
)
