import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='Snookey2',
      author='IOnlyPlayAsDrift',
      version='3.1.1',
      description='Stream on RPAN on PC easily using OBS and this module!',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/IOnlyPlayAsDrift/Snookey2',
      install_requires=[
          'pytz',
          'requests', 
          'pypresence',
          'praw'
      ],
      py_modules = ['snookey2'],
      entry_points={'console_scripts': ['snookey=snookey2:main']}
      ) 
