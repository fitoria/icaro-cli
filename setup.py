import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "icaro-cli",
    version = "0.1",
    author = "Adolfo Fitoria",
    author_email = "adolfo@fitoria.net",
    description = 'Herramientas de linea de comandos para icaro',
    license = "BSD",
    keywords = "console icaro",
    packages=find_packages(),
    long_description=read('README'),
    install_requires=['pyusb'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points = {
        'console_scripts' : [
            'icaro-cli = icaro_cli:main',
        ]
    },
)
