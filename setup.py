from setuptools import setup, find_packages

setup(
    name='enzymes',
    version='0.0.1',
    url='https://github.com/agriuseatstweets/enzymes',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'toolz',
        'numpy',
        'scipy'
    ]
)
