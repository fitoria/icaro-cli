import os
from setuptools import setup, find_packages



setup(
    name = "icaro-cli",
    version = "0.1",
    author = "Adolfo Fitoria",
    author_email = "adolfo@fitoria.net",
    description = 'Herramientas de linea de comandos para ICARO',
    license = "BSD",
    keywords = "console icaro",
    packages=find_packages(),
    long_description='HHerramientas de linea de comandos para ICARO',
    install_requires=['pyusb==1.0.0', 'pystache==0.5.4'],
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
