from os import path
from setuptools import setup, find_packages


with open(path.join(path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()


setup(
    name="django-label-templates",
    version='1.0.2',
    license="MIT",

    # packaging
    install_requires=['Django>=1.8', 'django-choices'],
    include_package_data=True,
    packages=find_packages(),

    # tests
    test_suite='runtests.runtests',
    tests_require=['coverage'],

    # metadata
    description="Load templates from site labels if available",
    long_description=readme,
    author="Maykin Media, Sergei Maertens",
    author_email="sergei@maykinmedia.nl",
    url="https://github.com/maykinmedia/django-label-templates",
    classifiers=[
       "Development Status :: 5 - Production/Stable",
       "Operating System :: OS Independent",
       "License :: OSI Approved :: MIT License",
       "Intended Audience :: Developers",
       "Framework :: Django",
       "Framework :: Django :: 1.8",
       "Framework :: Django :: 1.9",
       "Programming Language :: Python :: 2.7",
       "Programming Language :: Python :: 3.3",
       "Programming Language :: Python :: 3.4",
       "Programming Language :: Python :: 3.5",
       "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
