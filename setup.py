import io
from setuptools import setup, find_packages

long_description = (
    io.open('README.rst', encoding='utf-8').read()
    + '\n' +
    io.open('CHANGES.txt', encoding='utf-8').read())

setup(name='more.marshmallow',
      version='0.1dev0',
      description="Marshmallow (de)serialization support for Morepath",
      long_description=long_description,
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      keywords='morepath',
      license="BSD",
      url="https://github.com/morepath/more.marshmallow",
      namespace_packages=['more'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
      ],
      install_requires=[
          'setuptools',
          'morepath >= 0.15',
          'marshmallow'
      ],
      extras_require=dict(
          test=[
              'pytest >= 2.9.0',
              'pytest-remove-stale-bytecode',
              'webtest'
          ],
          coverage=[
              'pytest-cov',
          ],
          pep8=[
              'flake8',
          ],
      ))
