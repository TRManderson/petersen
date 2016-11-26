"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages

install_requires = [
    'sqlalchemy',
    'flask',
    'typing',
    'mako',
]

setup(
    name='petersen',
    version='0.0.1',
    description='Social network framework for creating positive impact communities',
    url='https://github.com/TRManderson/petersen',
    author='Lewis Bobbermen, Tom Manderson, Neil Ashford',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(),
    install_requires=install_requires,
)
