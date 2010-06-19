from setuptools import setup, find_packages
import os

version = '1.0'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

description_parts = (
    read("README.rst"),
    '',
    read("transmogrify", "comments", "README.rst"),
    '',
    read("docs", "HISTORY.rst"),
    '',
    )
long_description = "\n".join(description_parts)

setup(
    name='transmogrify.comments',
    version=version,
    description="A transmogrifier blueprint to migrate comments into Plone",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
    keywords='transmogrifier migration comments plone',
    author='Clayton Parker',
    author_email='robots@claytron.com',
    url='http://github.com/claytron/transmogrify.comments',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['transmogrify'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.transmogrifier',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
