from setuptools import setup
from os import path

requirements = [
    'numpy',
    'pandas',
    'matplotlib',
    'scipy',
    'scikit-optimize',
    'pyswarms',
    'pymc3',
]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='epidemia',
      version='0.0.3',
      description='Modelling COVID-19 using SIR-like models',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/COVID19-CMM/Epidemia',
      author='Taco de Wolff',
      author_email='tacodewolff@gmail.com',
      license='MIT',
      packages=['epidemia'],
      keywords=['epidemic', 'SIR', 'SEIR', 'COVID-19', 'corona', 'virus', 'compartmental'],
      python_requires='>=3.6',
      install_requires=requirements,
)
