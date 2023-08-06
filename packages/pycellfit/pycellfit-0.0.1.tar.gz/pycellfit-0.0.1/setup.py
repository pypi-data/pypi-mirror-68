from setuptools import setup, find_packages

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

# todo: edit to include all dependencies
requirements = ['numpy>=1.18']

setup(
    name='pycellfit',
    version='0.0.1',
    license='MIT',
    author='Nilai Vemula',
    author_email='nilai.r.vemula@vanderbilt.edu',
    description='Python implementation of the CellFIT method of inferring cellular forces',
    #long_description=readme,
    url='https://github.com/NilaiVemula/PyCellFIT',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Natural Language :: English"
    ],
)
