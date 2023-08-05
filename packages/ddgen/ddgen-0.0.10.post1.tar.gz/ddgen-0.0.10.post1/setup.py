from setuptools import setup, find_packages

import ddgen
from ddgen.db.h2 import supported_h2_versions

# read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# read description
with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(name='ddgen',
      version=ddgen.__version__,
      packages=find_packages(),
      install_requires=requirements,

      long_description=long_description,
      long_description_content_type='text/markdown',

      author='Daniel Danis',
      author_email='daniel.gordon.danis@gmail.com',
      url='https://github.com/ielis/ddgen',
      description='Library of Python utilities that I needed so many times',
      license='GPLv3',
      keywords='bioinformatics genomics',

      package_data={
          '': ['test_data/*'],
          'ddgen': ['utils/data/hg19.dict',
                    'utils/data/hg38.dict'] +
                   ['db/jar/h2-{}.jar'.format(version) for version in supported_h2_versions]},
      data_files=[('', ['requirements.txt'])]

      )
