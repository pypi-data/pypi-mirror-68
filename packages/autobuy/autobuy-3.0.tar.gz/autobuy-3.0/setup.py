from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='autobuy',
      description='An unofficial Python wrapper for the autobuy.io API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      version='3.0',
      url='https://github.com/jakestrouse00/AutoBuy.io-Python-Wrapper',
      author='Jake Strouse',
      author_email='jakestrouse00@gmail.com',
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Affero General Public License v3",
          "Operating System :: OS Independent",
      ],
      install_requires=['requests==2.22.0'],
      python_requires='>=3.6')
