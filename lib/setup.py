from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    long_description = f.read()

setup(name='poitousprint',
      version='0.0.1',
      description='A library to facilitate data manipulation for the Poitou sprint!',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/medialab/portic-datasprint-2021',
      license='MIT',
      author='Cécile Asselin, Robin de Mourat',
      python_requires='>=3.5',
      packages=find_packages(),
      install_requires=[
        'networkx',
        'requests'
      ],
      zip_safe=True)
