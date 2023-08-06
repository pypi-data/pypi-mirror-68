from setuptools import setup
import os
import stepic

version = stepic.__version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='stepic',
      version=version,
      description='Python image steganography',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Lenny Domnitser',
      author_email='lenny@domnit.org',
      maintainer="Scott Kitterman",
      maintainer_email="scott@kitterman.com",
      url='https://launchpad.net/stepic',
      license='GPL',
      packages=['stepic'],
      entry_points={
          'console_scripts' : [
              'stepic = stepic:main',
          ],
      },
      install_requires=['pillow',],
      include_package_data=True,
      zip_safe=False,
      data_files=[(os.path.join('share', 'man', 'man1'), ['stepic.1'])],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Environment :: Console',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Utilities',
          'Development Status :: 6 - Mature',
          'Programming Language :: Python :: 3 :: Only'
          ]
      )
