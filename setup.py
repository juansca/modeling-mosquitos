from setuptools import find_packages, setup

setup(
    name="mosquitomodeling",
    description="Framework to tune parameters and fit models for mosquito space-temporal modeling",
    url="https://github.com/juansca/modeling-mosquitos",
    author="Juan M. Scavuzzo, Francisco C. Trucco",
    author_email="jscavuzzo@machinalis.com",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "tabulate==0.8.2",
        "docopt==0.6.2",
        "numpy==1.14.5",
        "matplotlib==2.2.2",
        "scikit-learn==0.19.2",
        "scipy==1.1.0",
        "pandas==0.23.4",
        "seaborn==0.8.1",
        "rpy2==2.9.4",
        "tzlocal==1.5.1"
    ],
    setup_requires=["pytest-runner==2.11.1", "wheel==0.29.0"],
    tests_require=["pytest==3.6.3", "pytest-mock==1.10.0"],
)
