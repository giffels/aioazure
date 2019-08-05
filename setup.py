from setuptools import setup, find_packages
import os

repo_base_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(repo_base_dir, 'README.md'), 'r') as read_me:
    long_description = read_me.read()

setup(
    name='aioazure',
    version='0.1.0',
    description='Very thin Python Azure Compute client using asyncio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/giffels/aioazure',
    author='Manuel Giffels',
    author_email='giffels@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Utilities',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='asyncio azure compute client',
    packages=find_packages(exclude=['tests']),
    install_requires=['simple-rest-client'],
    tests_require=['flake8'],
    zip_safe=False,
    test_suite='tests',
    project_urls={
        'Bug Reports': 'https://github.com/giffels/aioazure/issues',
        'Source': 'https://github.com/giffels/aioazure',
    },
)
