from distutils.core import setup
#from Cython.Build import cythonize

from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop

requirements = [
    "pandas >= 0.15.0",
    "numpy >= 1.0.0",
    "scikit-learn >= 0.15",
    "scipy >= 0.10.0",
    "sarge >= 0.1.1",
    "lxml >= 3.6.0",
    "bs4 >= 0.0.0.1",
    "matplotlib >= 1.5",
]

setup(name='trectools',
        version='0.0.44',
        author='Joao Palotti',
        author_email='joaopalotti@gmail.com',
        license='BSD',
        install_requires=requirements,
        packages=['trectools'],
        #package_dir = {'': '.'},
        url='https://github.com/joaopalotti/trec_tools',
        description='An open-source Python library for assisting Information Retrieval (IR) practitioners with TREC-like campaigns.',
        long_description=open('README.txt').read()
)

