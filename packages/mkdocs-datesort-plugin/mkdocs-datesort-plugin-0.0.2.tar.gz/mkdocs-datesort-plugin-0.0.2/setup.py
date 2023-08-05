from setuptools import setup, find_packages

setup(
    name='mkdocs-datesort-plugin',
    version='0.0.2',
    description="Mkdocs datesort plugin",
    url="https://github.com/kubilus1/mkdocs-datesort-plugin",
    author='Matt Kubilus',
    install_requires=[
        'mkdocs>=0.17',
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'datesort = datesort.plugin:DatesortPlugin'
        ]
    }
)
