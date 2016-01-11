from os import path
from setuptools import setup, find_packages


with open(path.join(path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()


setup(
    name="django-label-templates",
    version='1.0.0',
    license="MIT",
    description="Load templates from site labels if available",
    long_description=readme,
    install_requires=['Django>=1.8'],
    # test_suite='runtests.get_suite',
    url="https://github.com/maykinmedia/django-label-templates",
    author="Maykin Media, Sergei Maertens",
    author_email="sergei@maykinmedia.nl",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
       "Development Status :: 5 - Production/Stable",
       "Operating System :: OS Independent",
       "License :: OSI Approved :: MIT License",
       "Intended Audience :: Developers",
       "Framework :: Django",
       "Programming Language :: Python :: 2.7",
       "Programming Language :: Python :: 3.3",
       "Programming Language :: Python :: 3.4",
       "Programming Language :: Python :: 3.5",
       "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
