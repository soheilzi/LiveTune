from setuptools import setup, find_packages

setup(
    name="LiveTune",
    version="0.0.1",
    author="Aiden Tabrizi, Soheil Zibakhsh",
    author_email="taiden@ucsd.edu, szibakhshshabgahi@ucsd.edu",
    description="Python package for ML developers and researchers to change certain variables while their code is executing to make the task of training a ML project easier. This package will allow you to tune some parameters while your code is live from outside of the program.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/soheilzi/LiveTune",
    entry_points={
        'console_scripts': [
            'updateVar=LiveTune.tools.updateVar:main',
        ],
    },
)
