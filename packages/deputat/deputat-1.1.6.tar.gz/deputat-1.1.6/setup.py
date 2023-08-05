from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='deputat',
    version='1.1.6',
    description='deputat overview',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lfreist/deputat",
    author='lfreist',
    author_email='freist.leon@gmx.de',
    packages=find_packages(),
    package_data={'deputat': ['GUI/pictures/*.svg', 'data/*.json']},
    install_requires=[
              'PyQt5',
              'distro',
              'openpyxl',
              'pandas',
              ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)
